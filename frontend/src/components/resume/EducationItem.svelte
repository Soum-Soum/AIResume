<script lang="ts">
    import {Education} from "../../api/data_objects";
    import type {z} from "zod";
    let {education}: {education: z.infer<typeof Education>} = $props();

    let degreeStr = $derived.by(() => {
        if (education.degree && education.field_of_study) {
            return `${education.degree} en ${education.field_of_study}`;
        } else if (education.degree) {
            return education.degree;
        } else if (education.field_of_study) {
            return education.field_of_study;
        }
        return '';
    })
</script>

<div class="p-4 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-300">
    <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-2">
        <h4 class="text-lg font-medium text-gray-800">{degreeStr}</h4>
        <span class="text-xs px-3 py-1 bg-blue-50 text-blue-800 rounded-full font-medium">
            {education.start_date} - {education.end_date}
        </span>
    </div>
    <p class="text-sm text-blue-700 font-medium mt-2">{education.institution}</p>
    {#if education.description}
        <p class="text-sm text-gray-600 mt-3 leading-relaxed">{education.description}</p>
    {/if}
</div>