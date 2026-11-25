import { required } from "@/shared/required";
import { exposeToEmbeddingPage, portFromEmbeddingPage } from "@/replay/messages";
import { fetchRecording, requestedVisualization, showUsage } from "@/replay/viewer/page";
import { showRecording } from "@/replay/viewer/rerun";
import { ReplaySession } from "@/replay/viewer/session";

const embeddingPage = portFromEmbeddingPage();
const parent = required(document.documentElement, "the replay page").child<HTMLElement>("#viewer", "an element with the id viewer");
const visualization = requestedVisualization();

if (visualization === "") showUsage(parent);
else await replay(visualization);

async function replay(visualization: string): Promise<void> {
    const contents = await fetchRecording(visualization);
    const viewer = await showRecording({ parent, name: visualization, contents });
    const session = await ReplaySession.open(viewer);
    await session.start();
    exposeToEmbeddingPage(session, await embeddingPage);
}
