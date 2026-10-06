# Scrollable video rail and Imagine image removal

## Scope

On the homepage, keep the video-card rail moving automatically while making it manually scrollable with a visible horizontal scrollbar. Remove the “my school bag walking to school by itself” picture from the Imagine image rail. Do not change other card images, captions, or video playback.

## Approaches considered

- Selected: drive the video rail's position through its native horizontal scroll offset and provide a visible scroll control beneath it. The existing repeated card group provides a seamless loop. Native overflow supports touch, trackpad, mouse-wheel/shift-wheel, and keyboard scrolling even where the system hides scrollbars.
- Rejected: leave the CSS transform animation in place and overlay a separate scroll control. The animation and manual scroll offsets would compete, causing jumps and making the scrollbar position misleading.

## Interaction

The video rail advances steadily when idle. During manual scrolling, pointer interaction, hover/focus, or video playback, automatic advancement pauses. It resumes two seconds after manual scrolling ends, but remains paused while a video plays or the pointer/focus is still in the rail. At the loop boundary, the scroll offset wraps to the matching repeated group without a visible jump. The rail has a visible horizontal scroll control even on systems that hide native scrollbars; the cards remain clickable and playable.

Users who request reduced motion do not get automatic advancement but can still scroll manually. On narrow screens, the cards remain a swipeable horizontal strip. The accessible label and native keyboard scrolling remain available.

The Imagine rail retains its current automatic animation. Remove both copies of the school-bag figure from its repeated image sequence so it does not return when the rail loops. Do not delete the underlying image asset or alter other uses of it outside that rail.

## Verification

Update the existing video-rail tests for scroll-driven looping, manual-control pause/resume, reduced-motion behavior, and video-playback pause. Check that the Imagine rail contains no school-bag figure and that the two repeated groups remain identical. Run the site test suite and inspect the changed markup, script, and responsive styles.
