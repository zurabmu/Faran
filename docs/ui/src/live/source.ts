import { required } from "@/shared/required";

/**
 * Returns the code of the code block that a `/// live` block holds inside `host`.
 */
export function sourceOf(host: HTMLElement): string {
    const code = required(host, `the live snippet "${host.getAttribute("caption")}"`).child(".highlight code", "a code block");
    return (code.textContent ?? "").replace(/\n$/, "");
}
