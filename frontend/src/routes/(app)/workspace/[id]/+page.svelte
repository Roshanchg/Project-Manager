<script lang="ts">
	import { page } from '$app/state';
	import { onMount } from 'svelte';

	const workspaceId = $derived(page.params.id);
    onMount(()=>{
        
    });
</script>

<h1>Workspace: {workspaceId}</h1>
<p>Boards for this workspace will go here.</p>
