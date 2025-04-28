<script lang="ts">
    import {Experience} from "../../api/data_objects";
    import type {z} from "zod";
    
    export let exp: z.infer<typeof Experience>;
</script>

<div class="p-4 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-300">
    <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-2">
        <h4 class="text-lg font-medium text-gray-800">{exp.title}</h4>
        <span class="text-xs px-3 py-1 bg-blue-50 text-blue-800 rounded-full font-medium">
            {exp.start_date} - {exp.end_date}
        </span>
    </div>
    <p class="text-sm text-blue-700 font-medium mt-2">{exp.company}, {exp.location}</p>
    {#if exp.description}
        <p class="text-sm text-gray-600 mt-3 leading-relaxed">{exp.description}</p>
    {/if}
</div>