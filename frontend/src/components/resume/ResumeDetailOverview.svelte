<script lang="ts">
    import ResumeGeneralInfo from "./ResumeGeneralInfo.svelte";
    import ExperienceItem from "./ExperienceItem.svelte";
    import EducationItem from "./EducationItem.svelte";
    import SkillItem from "./SkillItem.svelte";
    import { createQuery } from '@tanstack/svelte-query';
    import { resumeApi} from "../../api/client";

    export let resumeId: string;
    $: resumeDetailQuery = createQuery({
        queryKey: ['resume.detail', resumeId],
        queryFn: ({ queryKey }) => resumeApi.getResume(queryKey[1]),
        enabled: !!resumeId
    })

</script>

{#if $resumeDetailQuery.isLoading}
    <p>Loading...</p>
{:else if $resumeDetailQuery.isError}
    <p>Error: {$resumeDetailQuery.error.message}</p>
{:else if $resumeDetailQuery.isSuccess}
    <div class="bg-white shadow-md rounded-2xl p-6 border border-gray-100
                transition-all duration-300 transform hover:shadow-xl">

        <!-- Informations générales -->
        <ResumeGeneralInfo resume={$resumeDetailQuery.data} />

        <!-- Section Expérience -->
        {#if $resumeDetailQuery.data.experience && $resumeDetailQuery.data.experience.length > 0}
            <div class="mb-6">
                <h3 class="text-lg font-semibold text-gray-800 mb-3">Expérience professionnelle</h3>
                <div class="space-y-4">
                    {#each $resumeDetailQuery.data.experience as exp (exp.id)}
                        <ExperienceItem {exp} />
                    {/each}
                </div>
            </div>
        {/if}

        <!-- Section Éducation -->
        {#if $resumeDetailQuery.data.education && $resumeDetailQuery.data.education.length > 0}
            <div class="mb-6">
                <h3 class="text-lg font-semibold text-gray-800 mb-3">Formation</h3>
                <div class="space-y-4">
                    {#each $resumeDetailQuery.data.education as edu (edu.id)}
                        <EducationItem {edu} />
                    {/each}
                </div>
            </div>
        {/if}

        <!-- Section Compétences -->
        {#if $resumeDetailQuery.data.skills && $resumeDetailQuery.data.skills.length > 0}
            <div>
                <h3 class="text-lg font-semibold text-gray-800 mb-3">Compétences</h3>
                <div class="flex flex-wrap gap-2">
                    {#each $resumeDetailQuery.data.skills as skill (skill.id)}
                        <SkillItem {skill} />
                    {/each}
                </div>
            </div>
        {/if}
    </div>
{:else}
    <p>Unknown state</p>
{/if}



<style lang="postcss">
    /* Styles supplémentaires si nécessaire */
</style>
