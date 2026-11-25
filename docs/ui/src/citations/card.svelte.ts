import * as hoverCard from "@zag-js/hover-card";
import { normalizeProps, useMachine } from "@zag-js/svelte";
import type { Attachment } from "svelte/attachments";
import { copiesOf } from "@/shared/dom/copies";
import { listen, stopAll } from "@/shared/dom/events";
import { RootNode } from "@/shared/dom/root";
import { referenceOf } from "@/citations/reference";

const CLOSE_DELAY = 160;
const GAP = 8;
const POSITIONING = { placement: "top-start", strategy: "fixed", gutter: GAP, overflowPadding: GAP } as const;

/**
 * The card that shows the reference of a citation while the pointer or the focus is on it.
 * Create it while a component initializes.
 */
export class CitationCard {
    readonly root = new RootNode();
    readonly api: hoverCard.Api;
    readonly #host: HTMLElement;

    constructor({ id, host }: { id: string; host: HTMLElement }) {
        this.#host = host;
        const service = useMachine(hoverCard.machine, () => ({
            id,
            getRootNode: this.root.get,
            openDelay: 0,
            closeDelay: CLOSE_DELAY,
            positioning: POSITIONING,
        }));
        this.api = $derived(hoverCard.connect(service, normalizeProps));
    }

    /**
     * Fills the card with copies of the reference.
     */
    readonly showReference: Attachment<HTMLElement> = (card) => copiesOf([...referenceOf(this.#host).childNodes])(card);

    /**
     * Opens the card while the focus is inside the citation.
     */
    readonly openOnFocus: Attachment<HTMLElement> = (citation) => {
        // Svelte's event handlers miss focus events from the slotted link, so the citation listens natively.
        return stopAll([listen(citation, "focusin", () => this.api.setOpen(true), {}), listen(citation, "focusout", () => this.api.setOpen(false), {})]);
    };

    /**
     * Shows the positioner as a popover while the card is open.
     */
    readonly showWhileOpen: Attachment<HTMLElement> = (positioner) => {
        $effect(() => {
            if (this.api.open) positioner.showPopover();
            else if (positioner.matches(":popover-open")) positioner.hidePopover();
        });
    };
}
