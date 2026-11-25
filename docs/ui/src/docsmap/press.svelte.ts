/**
 * Runs a CSS press animation through the `pressed` class. Pressing again while the animation
 * runs starts it over in the next animation frame.
 */
export class PressAnimation {
    pressed = $state(false);

    press(): void {
        this.pressed = false;
        requestAnimationFrame(() => (this.pressed = true));
    }

    end(): void {
        this.pressed = false;
    }
}
