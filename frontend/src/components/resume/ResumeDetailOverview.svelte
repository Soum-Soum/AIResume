<script lang="ts">
    import ResumeGeneralInfo from "./ResumeGeneralInfo.svelte";
    import ExperienceItem from "./ExperienceItem.svelte";
    import EducationItem from "./EducationItem.svelte";
    import SkillItem from "./SkillItem.svelte";
    import {createQuery} from '@tanstack/svelte-query';
    import {resumeApi} from "../../api/client";

    let {resumeId} = $props();
    let resumeDetailQuery = $derived(
        createQuery({
            queryKey: ['resume.detail', resumeId],
            queryFn: ({queryKey}) => resumeApi.getResume(queryKey[1]),
            enabled: !!resumeId
        })
    );
</script>

{#if $resumeDetailQuery.isLoading}
    <div class="flex justify-center items-center min-h-32">
        <div class="animate-pulse text-blue-600">Chargement...</div>
    </div>
{:else if $resumeDetailQuery.isError}
    <div class="bg-red-50 text-red-700 p-4 rounded-lg border border-red-200">
        <p>Erreur: {$resumeDetailQuery.error.message}</p>
    </div>
{:else if $resumeDetailQuery.isSuccess}
    <div class="bg-white shadow-lg rounded-3xl p-8 border border-gray-100
                transition-all duration-300 hover:shadow-xl max-w-4xl mx-auto">

        <!-- Informations générales -->
        <ResumeGeneralInfo resume={$resumeDetailQuery.data}/>

        <!-- Section Expérience -->
        <div class="mb-8">
            <h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                <span class="mr-2 text-blue-600">💼</span>Expérience professionnelle
            </h3>
            <div class="space-y-4">
                {#each $resumeDetailQuery.data.experiences as exp (exp.id)}
                    <ExperienceItem {exp}/>
                {/each}
            </div>
        </div>

        <!-- Section Éducation -->
        <div class="mb-8">
            <h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                <span class="mr-2 text-blue-600">🎓</span>Formation
            </h3>
            <div class="space-y-4">
                {#each $resumeDetailQuery.data.educations as education (education.id)}
                    <EducationItem {education}/>
                {/each}
            </div>
        </div>

        <!-- Section Compétences -->
        <div>
            <h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                <span class="mr-2 text-blue-600">🔧</span>Compétences
            </h3>
            <div class="flex flex-wrap gap-3">
                {#each $resumeDetailQuery.data.skills as skill (skill.id)}
                    <SkillItem {skill}/>
                {/each}
            </div>
        </div>
    </div>
{:else}
    <p class="text-gray-700 italic">État inconnu</p>
{/if}

<style lang="postcss">
    /* Les styles sont maintenant intégrés directement dans les classes Tailwind */
</style>