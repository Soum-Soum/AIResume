<script lang="ts">
    import {ResumeWithDetails} from "../../api/data_objects";
    import type {z} from "zod";
    
    export let resume: z.infer<typeof ResumeWithDetails>;
</script>

<div class="mb-6 border-b pb-4">
    <h2 class="text-2xl font-bold text-gray-800">{resume.name}</h2>
    <div class="mt-2 space-y-1">
        <p class="text-sm text-gray-600 flex items-center gap-2">
            <span>📧</span> {resume.email}
        </p>
        {#if resume.phone}
            <p class="text-sm text-gray-600 flex items-center gap-2">
                <span>📞</span> {resume.phone}
            </p>
        {/if}
    </div>
    {#if resume.summary}
        <div class="mt-4">
            <h3 class="text-md font-semibold text-gray-700">Résumé</h3>
            <p class="text-sm text-gray-600 mt-1">{resume.summary}</p>
        </div>
    {/if}
</div>
