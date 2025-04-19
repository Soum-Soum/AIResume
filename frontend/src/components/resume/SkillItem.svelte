<script lang="ts">
    import {Skill} from "../../api/data_objects";
    import type {z} from "zod";
    
    export let skill: z.infer<typeof Skill>;
</script>

<div class="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
    {skill.name}
    <span class="text-xs ml-1">({skill.level})</span>
</div>
