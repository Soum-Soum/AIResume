<script lang="ts">
    import {ResumeWithDetails} from "../../api/data_objects";
    import type {z} from "zod";
    
    export let resume: z.infer<typeof ResumeWithDetails>;
</script>

<div class="mb-8 border-b border-gray-200 pb-6">
    <h2 class="text-3xl font-bold text-gray-800 mb-3">{resume.name}</h2>
    <div class="flex flex-wrap gap-4 mb-4">
        <p class="text-sm text-gray-700 flex items-center gap-2 bg-gray-50 px-3 py-1 rounded-md">
            <span class="text-blue-600">📧</span> {resume.email}
        </p>
        {#if resume.phone}
            <p class="text-sm text-gray-700 flex items-center gap-2 bg-gray-50 px-3 py-1 rounded-md">
                <span class="text-blue-600">📞</span> {resume.phone}
            </p>
        {/if}
    </div>
    {#if resume.summary}
        <div class="mt-5 bg-gray-50 p-4 rounded-lg border-l-4 border-blue-500">
            <h3 class="text-md font-semibold text-gray-800 mb-2">À propos</h3>
            <p class="text-gray-700 leading-relaxed">{resume.summary}</p>
        </div>
    {/if}
</div>