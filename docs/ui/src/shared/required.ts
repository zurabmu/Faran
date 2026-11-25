/**
 * Finds elements around one element that the page must contain. Throws when one is missing.
 */
export class RequiredElements {
    constructor(
        private readonly element: Element,
        private readonly description: string,
    ) {}

    /**
     * Returns the first descendant that matches `selector`. `what` describes it in the error.
     */
    child<Found extends Element = Element>(selector: string, what: string): Found {
        const found = this.element.querySelector<Found>(selector);
        if (found === null) throw new Error(`Expected ${this.description} to hold ${what}, but it has none.`);
        return found;
    }

    /**
     * Returns the closest ancestor that matches `selector`. `what` describes it in the error.
     */
    ancestor<Found extends Element = Element>(selector: string, what: string): Found {
        const found = this.element.parentElement?.closest<Found>(selector);
        if (found === null || found === undefined) throw new Error(`Expected ${this.description} to be inside ${what}, but it is not.`);
        return found;
    }

    /**
     * Returns the next sibling element, which must match `selector`. `what` describes it in the
     * error.
     */
    next<Found extends Element = Element>(selector: string, what: string): Found {
        const sibling = this.element.nextElementSibling;
        if (sibling === null || !sibling.matches(selector)) throw new Error(`Expected ${this.description} to be followed by ${what}, but it is not.`);
        return sibling as Found;
    }
}

/**
 * Returns the required elements around `element`, which errors call `description`, such as
 * "the live snippet Bicycle".
 */
export function required(element: Element, description: string): RequiredElements {
    return new RequiredElements(element, description);
}
