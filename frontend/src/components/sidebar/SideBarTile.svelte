<script lang="ts">
    import {Resume} from "../../api/data_objects";
    import type { z } from "zod";

    let {resume}: {resume: z.infer<typeof Resume>} = $props()
</script>

<button
    class="text-left max-w-sm w-full bg-white shadow-md rounded-2xl p-3 border border-gray-100
           transition-all duration-300 transform hover:shadow-2xl hover:-translate-y-1 hover:scale-[1.02]"
>
    <div class="space-y-0.5">
        <p class="text-sm font-semibold text-gray-800">{resume.name}</p>
        <p class="text-xs text-gray-400 flex items-center gap-2">
            <span>📞</span> {resume.phone || 'N/A'}
        </p>
        <p class="text-xs text-gray-400 flex items-center gap-2">
            <span>📧</span> {resume.email}
        </p>
    </div>
</button>

<style lang="postcss">

</style>