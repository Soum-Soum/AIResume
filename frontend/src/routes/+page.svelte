<script>
    import { QueryClientProvider } from '@tanstack/svelte-query';
    import { queryClient } from "$lib/query-client";
    import Page from "../components/Page.svelte";
</script>

<QueryClientProvider client={queryClient}>
    <Page></Page>
</QueryClientProvider>

