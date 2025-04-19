import { QueryClient } from '@tanstack/svelte-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30000,  //Considered fresh for 30 seconds
      refetchOnWindowFocus: true,  // Refetch on window focus
      retry: 1  // Retry failed requests once
    }
  }
});