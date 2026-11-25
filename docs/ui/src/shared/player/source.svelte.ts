/**
 * Whether a player's source panel is open, and whether it was ever opened, so that its
 * content is created on first use.
 */
export class SourcePanel {
    open = $state(false);
    requested = $state(false);

    toggle(): void {
        this.open = !this.open;
        if (this.open) this.requested = true;
    }
}
