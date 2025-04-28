<script lang="ts">
    import {Skill} from "../../api/data_objects";
    import type {z} from "zod";
    
    export let skill: z.infer<typeof Skill>;
</script>

<div class="px-4 py-2 bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-800 rounded-lg shadow-sm
            border border-blue-100 transition-all duration-200 hover:shadow-md hover:scale-105 text-sm">
    <span class="font-medium">{skill.name}</span>
    <span class="text-xs ml-2 opacity-80">({skill.level})</span>
</div>