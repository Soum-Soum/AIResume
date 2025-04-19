<script>
    import SideBar from "./sidebar/SideBar.svelte";
    import {selectedResumeId} from "$lib/stores/selectedResume.js";
    import ResumeDetailOverview from "./resume/ResumeDetailOverview.svelte";
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <!-- Header -->
    <header class="bg-red-500 p-4">(header)</header>
    <!-- Grid Columns -->
    <div class="grid grid-cols-1 md:grid-cols-[auto_1fr]">
        <!-- Left Sidebar. -->
        <aside class="mx-4 mt-2">
            <SideBar/>
        </aside>
        <!-- Main Content -->
        {#if ($selectedResumeId !== null)}
            <main class="space-y-4 bg-green-500 p-4">
                <p>{$selectedResumeId}</p>
                <ResumeDetailOverview resumeId={$selectedResumeId}/>
            </main>
        {:else}
            <main class="space-y-4 bg-green-500 p-4">
                <p class="h-[512px] bg-purple-500 p-4">Paragraph 1</p>
                <p class="h-[512px] bg-purple-500 p-4">Paragraph 2</p>
                <p class="h-[512px] bg-purple-500 p-4">Paragraph 3</p>
            </main>
        {/if}

    </div>
    <!-- Footer -->
    <footer class="bg-blue-500 p-4">(footer)</footer>
</div>
