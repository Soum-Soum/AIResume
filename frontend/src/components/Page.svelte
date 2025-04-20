<script>
    import SideBar from "./sidebar/SideBar.svelte";
    import ResumeDetailOverview from "./resume/ResumeDetailOverview.svelte";

    let selectedResumeId = $state("unset");
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <!-- Header -->
    <header class="bg-red-500 p-4">(header)</header>
    <!-- Grid Columns -->
    <div class="grid grid-cols-1 md:grid-cols-[auto_1fr]">
        <!-- Left Sidebar. -->
        <aside class="mx-4 mt-2">
            <SideBar bind:selectedResumeId={selectedResumeId}/>
        </aside>
        <!-- Main Content -->
        <main class="space-y-4 bg-green-500 p-4">
            {#if selectedResumeId !== "unset"}
                <ResumeDetailOverview resumeId={selectedResumeId} />
            {/if}
        </main>
    </div>
    <!-- Footer -->
    <footer class="bg-blue-500 p-4">(footer)</footer>
</div>
