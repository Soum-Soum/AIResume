<script lang="ts">
    import {Experience} from "../../api/data_objects";
    import type {z} from "zod";
    
    export let exp: z.infer<typeof Experience>;
</script>

<div class="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
    <div class="flex justify-between items-start">
        <h4 class="text-md font-medium text-gray-800">{exp.title}</h4>
        <span class="text-xs text-gray-500">{exp.start_date} - {exp.end_date}</span>
    </div>
    <p class="text-sm text-gray-700 mt-1">{exp.company}, {exp.location}</p>
    <p class="text-sm text-gray-600 mt-2">{exp.description}</p>
</div>
