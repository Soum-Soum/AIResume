<script lang="ts">
    import { selectedResumeId } from '../../lib/stores/selectedResume';

    export let id: string;
    export let name: string;
    export let phoneNumber: string;
    export let email: string;

    function handleClick() {
        selectedResumeId.set(id);
    }
</script>

<button
    class="text-left max-w-sm w-full bg-white shadow-md rounded-2xl p-3 border border-gray-100
           transition-all duration-300 transform hover:shadow-2xl hover:-translate-y-1 hover:scale-[1.02]"
    on:click={handleClick}
>
    <div class="space-y-0.5">
        <p class="text-sm font-semibold text-gray-800">{name}</p>
        <p class="text-xs text-gray-400 flex items-center gap-2">
            <span>📞</span> {phoneNumber}
        </p>
        <p class="text-xs text-gray-400 flex items-center gap-2">
            <span>📧</span> {email}
        </p>
    </div>
</button>

<style lang="postcss">

</style>