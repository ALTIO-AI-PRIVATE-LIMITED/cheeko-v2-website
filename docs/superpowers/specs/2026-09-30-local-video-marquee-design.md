# Local Video Marquee Design

## Goal

Replace the homepage Press play section's Instagram embeds with the unique local videos in `assets/updated-vids`, while retaining the existing 20-second Cheeko film. Every visible video card must have an appropriate poster, a clear play button, and working inline playback. The marquee must loop continuously from right to left.

## Scope

The finished marquee contains six unique videos:

1. Everything Cheeko Does (the existing 20-second film)
2. Hand Them Cheeko
3. No Tantrum
4. Built to END
5. Five Minutes
6. Parent App

The two Parent App MP4 files are byte-for-byte identical, so the video appears once. Its supplied poster is `V19 Parent App - thumbnail (1).jpg`.

No Instagram iframe remains in the section. No unrelated homepage section is changed.

## Markup and Media

Each primary card uses the same accessible structure:

- a local `<video>` with `preload="none"` and `playsinline`;
- a matching local `poster` image;
- a semantic `<button>` with a video-specific play label;
- the existing orange circular play icon; and
- no added caption overlay; the poster artwork remains unobstructed.

The existing 20-second film continues using its current video and poster. The five new cards reference files in `assets/updated-vids`. URL-encoded paths are used for filenames containing spaces.

The duplicate group required for the seamless loop contains the same playable cards so every card that rolls into view remains interactive. When reduced motion is requested, the duplicate group is removed and the primary group becomes a horizontally scrollable row.

## Marquee Motion

The two equal-width groups create a seamless loop. The animation runs from the origin to one negative group-width offset, making the cards travel right to left. It pauses when the user hovers over the marquee, focuses a control, or plays a video.

Playing a video pauses the track so the selected card does not move away. Pausing or ending playback releases the playback pause; normal hover or focus rules may still keep the track stationary. The reduced-motion media query disables automatic movement.

## Playback Behavior

The play button performs these steps from the user's click gesture:

1. pause any other video in the marquee;
2. expose native video controls;
3. request unmuted inline playback;
4. hide the play overlay only after playback succeeds; and
5. pause the marquee while the video is playing.

If `video.play()` rejects, the card returns to its poster state, the native controls remain available, and the play overlay remains visible. This prevents the current stuck state where the button disappears without confirmed playback.

Caption overlays are omitted, so the full play overlay remains unobstructed. When playback ends, the video returns to its poster state with the play button visible.

## Accessibility

- Each play button names its video.
- Both loop groups remain playable so the moving marquee never exposes an inert card.
- Keyboard focus pauses the marquee.
- Native controls are available after playback starts or when automatic start fails.
- Reduced-motion users receive a manually scrollable list instead of animation.

## Verification

Automated static tests will verify:

- all five unique updated videos and all available/generated posters are referenced;
- the existing 20-second film remains;
- no Instagram iframe remains in the Press play section;
- every primary video has a labeled play button;
- the animation direction is right to left;
- both groups contain complete playable cards, while reduced-motion mode removes the duplicate group;
- playback code does not force videos to remain muted; and
- rejected playback restores a usable card state.

Media inspection will verify that each referenced MP4 and poster exists and that every MP4 has a browser-compatible H.264 video stream. JavaScript syntax checks and the full static test suite will run before completion. If browser automation becomes available, a final interaction check will confirm that playback starts, sound is enabled, and marquee motion pauses.
