<script lang="ts">
    import { createQuery } from '@tanstack/svelte-query';
    import { resumeApi} from "../../api/client";
    import SideBarTile from "./SideBarTile.svelte";

	let { selectedResumeId = $bindable() } = $props();

    function handleClick(resumeId: string) {
        selectedResumeId = resumeId;
    }

    const resumeListQuery = createQuery({
        queryKey: ['resume.list'],
        queryFn: resumeApi.getResumes,
    })

</script>

<div class="grid grid-cols-1 gap-2">
    {#if $resumeListQuery.isLoading}
        <p>Loading...</p>
    {:else if $resumeListQuery.isError}
        <p>Error: {$resumeListQuery.error.message}</p>
    {:else if $resumeListQuery.isSuccess}
        {#each $resumeListQuery.data as resume (resume.id)}
            <div onclick={() => handleClick(resume.id)} class="cursor-pointer">
                <SideBarTile resume={resume}/>
            </div>
        {/each}
    {:else}
        <p>Unknown state</p>

    {/if}
</div>

<style lang="postcss">

</style>