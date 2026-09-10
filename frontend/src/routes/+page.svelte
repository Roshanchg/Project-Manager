<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	onMount(() => {
		goto(resolve('/dashboard'));
	});
</script>

<p>Redirecting...</p>
