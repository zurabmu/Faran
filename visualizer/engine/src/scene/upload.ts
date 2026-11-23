import type { InstancedBufferAttribute, InstancedInterleavedBuffer } from "three";

/**
 * Marks the first `floats` values of a buffer for upload to the GPU on the next render.
 */
export function markWritten(buffer: InstancedBufferAttribute | InstancedInterleavedBuffer, floats: number): void {
    const nothingWritten = floats === 0;
    if (nothingWritten) return;
    buffer.clearUpdateRanges();
    buffer.addUpdateRange(0, floats);
    buffer.needsUpdate = true;
}
