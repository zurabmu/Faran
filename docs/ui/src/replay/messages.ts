import { expose, proxy, type Remote, wrap } from "comlink";

const CONNECT_MESSAGE = "faran-replay:connect";

/**
 * What a replay page reports to the page that embeds it. `seconds` and `endSeconds` are
 * simulation time.
 */
export interface ReplayReport {
    readonly first: number;
    readonly last: number;
    readonly step: number;
    readonly seconds: number;
    readonly endSeconds: number;
    readonly playing: boolean;
}

/**
 * The commands that the embedding page sends to a replay page.
 */
export interface ReplayCommands {
    play(): Promise<void>;
    pause(): Promise<void>;

    /**
     * Pauses at `step`, clamped to the recorded steps.
     */
    seek(step: number): Promise<void>;

    /**
     * Sets the playback speed as a multiple of real time.
     */
    changeSpeed(speed: number): Promise<void>;

    /**
     * Restores the layout that the recording came with.
     */
    resetLayout(): Promise<void>;
}

/**
 * A replay page as the page that embeds it sees it. `subscribe` sends every later report to
 * `receive`.
 */
export interface ReplayPage extends ReplayCommands {
    subscribe(receive: (report: ReplayReport) => void): void;
}

/**
 * Connects to the replay page in `frame` and sends its reports to `receive`. Commands sent before
 * the replay page is ready wait until it is.
 */
export function connectToReplay({ frame, receive }: { frame: HTMLIFrameElement; receive: (report: ReplayReport) => void }): Remote<ReplayPage> {
    const channel = new MessageChannel();
    frame.addEventListener("load", () => sendPort(frame, channel.port2), { once: true });
    const page = wrap<ReplayPage>(channel.port1);
    void page.subscribe(proxy(receive));
    return page;
}

/**
 * Resolves with the port that the embedding page sends. Call it before this page finishes loading.
 */
export function portFromEmbeddingPage(): Promise<MessagePort> {
    return new Promise((resolve) => {
        const receive = (event: MessageEvent) => {
            const isConnection = event.origin === window.location.origin && event.data === CONNECT_MESSAGE;
            if (!isConnection) return;
            window.removeEventListener("message", receive);
            resolve(portOf(event));
        };
        window.addEventListener("message", receive);
    });
}

/**
 * Lets the embedding page use `page` through `port`.
 */
export function exposeToEmbeddingPage(page: ReplayPage, port: MessagePort): void {
    expose(page, port);
}

function sendPort(frame: HTMLIFrameElement, port: MessagePort): void {
    const target = frame.contentWindow;
    if (target === null) throw new Error(`Expected the replay frame ${frame.src} to have a page once it loaded, but it has none.`);
    target.postMessage(CONNECT_MESSAGE, window.location.origin, [port]);
}

function portOf(event: MessageEvent): MessagePort {
    const port = event.ports[0];
    if (port === undefined) throw new Error("Expected the embedding page to send a port with its connection message, but it sent none.");
    return port;
}
