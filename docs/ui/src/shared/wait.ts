/**
 * Resolves after `milliseconds`, once the event loop has handled the messages that arrived
 * meanwhile.
 */
export function wait(milliseconds: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, milliseconds));
}
