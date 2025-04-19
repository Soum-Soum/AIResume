<script lang="ts">
    import { createQuery } from '@tanstack/svelte-query';
    import { resumeApi} from "../../api/client";
    import SideBarTile from "./SideBarTile.svelte";

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
            <SideBarTile
                id={resume.id}
                name={resume.name}
                phoneNumber={resume.phone}
                email={resume.email}
            />
        {/each}
    {:else}
        <p>Unknown state</p>

    {/if}
</div>

<style lang="postcss">

</style>