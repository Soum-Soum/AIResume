<script lang="ts">
    import {Education} from "../../api/data_objects";
    import type {z} from "zod";
    
    export let edu: z.infer<typeof Education>;
</script>

<div class="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
    <div class="flex justify-between items-start">
        <h4 class="text-md font-medium text-gray-800">{edu.degree} en {edu.field_of_study}</h4>
        <span class="text-xs text-gray-500">{edu.start_date} - {edu.end_date}</span>
    </div>
    <p class="text-sm text-gray-700 mt-1">{edu.institution}</p>
    <p class="text-sm text-gray-600 mt-2">{edu.description}</p>
</div>
