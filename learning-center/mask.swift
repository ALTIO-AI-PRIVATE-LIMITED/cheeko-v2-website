// Subject masks with Apple Vision (the same "lift subject" the Photos app uses), so shadows and cut-outs keep
// white, blue and grey parts. Usage: swift mask.swift <out dir> <image>...   writes <out dir>/<name>.png (white = subject)
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
let outDir = URL(fileURLWithPath: args[1])
let ctx = CIContext()
for path in args.dropFirst(2) {
    let url = URL(fileURLWithPath: path)
    let name = url.deletingPathExtension().lastPathComponent
    let handler = VNImageRequestHandler(url: url, options: [:])
    let req = VNGenerateForegroundInstanceMaskRequest()
    do {
        try handler.perform([req])
        guard let obs = req.results?.first, !obs.allInstances.isEmpty else { print("none", name); continue }
        let buf = try obs.generateScaledMaskForImage(forInstances: obs.allInstances, from: handler)
        let ci = CIImage(cvPixelBuffer: buf)
        guard let cg = ctx.createCGImage(ci, from: ci.extent) else { print("fail", name); continue }
        let dest = CGImageDestinationCreateWithURL(outDir.appendingPathComponent(name + ".png") as CFURL, UTType.png.identifier as CFString, 1, nil)!
        CGImageDestinationAddImage(dest, cg, nil); CGImageDestinationFinalize(dest)
        print("ok", name, obs.allInstances.count)
    } catch { print("error", name, error) }
}
