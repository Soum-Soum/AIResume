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

<div class="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
    <div class="flex justify-between items-start">
        <h4 class="text-md font-medium text-gray-800">{degreeStr}</h4>
        <span class="text-xs text-gray-500">{education.start_date} - {education.end_date}</span>
    </div>
    <p class="text-sm text-gray-700 mt-1">{education.institution}</p>
    <p class="text-sm text-gray-600 mt-2">{education.description}</p>
</div>
