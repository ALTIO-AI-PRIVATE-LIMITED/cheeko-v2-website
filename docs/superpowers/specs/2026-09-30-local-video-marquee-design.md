# Local Video Marquee Design

## Goal

Replace the homepage Press play section's Instagram embeds with the unique local videos in `assets/updated-vids`, while retaining the existing 20-second Cheeko film. Every visible video card must have an appropriate poster, a clear play button, and working inline playback. The marquee must loop continuously from left to right.

## Scope

The finished marquee contains six unique videos:

1. Everything Cheeko Does (the existing 20-second film)
2. Hand Them Cheeko
3. No Tantrum
4. Built to END
5. Five Minutes
6. Parent App

The two Parent App MP4 files are byte-for-byte identical, so the video appears once. Because no Parent App thumbnail was supplied, a poster image will be extracted from that video and stored beside it in `assets/updated-vids`.

No Instagram iframe remains in the section. No unrelated homepage section is changed.

## Markup and Media

Each primary card uses the same accessible structure:

- a local `<video>` with `preload="none"` and `playsinline`;
- a matching local `poster` image;
- a semantic `<button>` with a video-specific play label;
- the existing orange circular play icon; and
- a short visible caption derived from the filename.

The existing 20-second film continues using its current video and poster. The five new cards reference files in `assets/updated-vids`. URL-encoded paths are used for filenames containing spaces.

The duplicate group required for the seamless loop uses poster-only, non-interactive copies. It is hidden from assistive technology and cannot receive keyboard focus. When reduced motion is requested, the duplicate group is removed and the primary group becomes a horizontally scrollable row.

## Marquee Motion

The two equal-width groups create a seamless loop. The animation runs from one group-width offset back to the origin, making the cards travel left to right. It pauses when the user hovers over the marquee, focuses a control, or plays a video.

Playing a video pauses the track so the selected card does not move away. Pausing or ending playback releases the playback pause; normal hover or focus rules may still keep the track stationary. The reduced-motion media query disables automatic movement.

## Playback Behavior

The play button performs these steps from the user's click gesture:

1. pause any other video in the marquee;
2. expose native video controls;
3. request unmuted inline playback;
4. hide the play overlay only after playback succeeds; and
5. pause the marquee while the video is playing.

If `video.play()` rejects, the card returns to its poster state, the native controls remain available, and the play overlay remains visible. This prevents the current stuck state where the button disappears without confirmed playback.

Captions do not intercept pointer input, so clicking anywhere on the full play overlay works. When playback ends, the video returns to its poster state with the play button visible.

## Accessibility

- Each play button names its video.
- Duplicate loop content is `aria-hidden` and non-interactive.
- Keyboard focus pauses the marquee.
- Native controls are available after playback starts or when automatic start fails.
- Reduced-motion users receive a manually scrollable list instead of animation.

## Verification

Automated static tests will verify:

- all five unique updated videos and all available/generated posters are referenced;
- the existing 20-second film remains;
- no Instagram iframe remains in the Press play section;
- every primary video has a labeled play button;
- the animation direction is left to right;
- duplicate content is poster-only and hidden from assistive technology;
- playback code does not force videos to remain muted; and
- rejected playback restores a usable card state.

Media inspection will verify that each referenced MP4 and poster exists and that every MP4 has a browser-compatible H.264 video stream. JavaScript syntax checks and the full static test suite will run before completion. If browser automation becomes available, a final interaction check will confirm that playback starts, sound is enabled, and marquee motion pauses.
