import { writable } from 'svelte/store';

export const selectedResumeId = writable<string | null>(null);