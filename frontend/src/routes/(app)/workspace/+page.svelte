<script lang="ts">
	import type { WorkspaceInfo } from '$lib/types';

	import WorkspaceCard from '$lib/components/layout/WorkspaceCard.svelte';
	let workspaces = $state<WorkspaceInfo[]>([
		{
			id: '1',
			name: 'Personal',
			color: '#4979E0',
			owner: 'Roshan',
			role: 'owner'
		},
		{
			id: '2',
			name: 'Work Projects',
			color: '#44CFA1',
			owner: 'Roshan',
			role: 'admin'
		},
		{
			id: '3',
			name: 'Shared Team',
			color: '#D7A246',
			owner: 'Someone Else',
			role: 'member'
		},
		{
			id: '4',
			name: 'Shared Team',
			color: '#E1B25F',
			owner: 'Someone Else',
			role: 'member'
		},
		{
			id: '5',
			name: 'Shared Team',
			color: '#AA8A52',
			owner: 'Someone Else',
			role: 'member'
		}
	]);
	function createNewWorkspace() {}
</script>

<h3>Workspaces</h3>
<span class="support-span">Manage Your Workspaces</span>
<div class="workspace-cards">
	{#each workspaces as workspace (workspace.id)}
		<WorkspaceCard
			workspace={workspace}
		></WorkspaceCard>
	{/each}
	<button class="insert-card" onclick={createNewWorkspace}>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 24 24"
			stroke-width="1.5"
			width="60px"
			height="60px"
			stroke="#f5f5f5"
			class="size-6"
			fill="#0051b8"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
			/>
		</svg>
		<span>Add New Workspace</span>
	</button>
</div>

<style>
	h3 {
		margin: 0;
		margin-bottom: 8px;
		font-size: 20px;
	}
	.support-span {
		font-weight: 550;
		opacity: 60%;
		font-size: 14px;
	}
	.workspace-cards {
		display: grid;
		padding-top: 1em;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 1.6em;
	}
	.insert-card {
		display: flex;
		align-items: center;
		flex-direction: column;
		justify-content: center;
		background-color: #f5f5f5;

		border-radius: 16px;
		border: 1px dashed #888888;
		outline: none;
		cursor: pointer;
		> span {
			font-weight: 540;
			font-size: 16px;
		}
	}
	.insert-card:hover {
		background-color: #f0f0f0;
	}
</style>
