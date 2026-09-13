<script lang="ts">
	import type { WorkspaceInfo } from '$lib/types';

	import WorkspaceCard from '$lib/components/layout/WorkspaceCard.svelte';
	import { userStore } from '$lib/stores/user.svelte';
	// let workspaceFormActive = $state(false);
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
	let formName = $state('');
	let dialogEl = $state<HTMLDialogElement | null>(null);
	let dialogueMode = $state<'create' | 'edit'>('create');
	let editingWorkspace = $state<WorkspaceInfo | null>(null);
	let formColor = $state('#4979E0');

	function openCreate() {
		formName = '';
		formColor = '#4979E0';
		dialogueMode = 'create';
		editingWorkspace = null;
		dialogEl?.showModal();
	}
	function closeCreate() {
		formName = '';
		formColor = '#4979E0';
		dialogEl?.close();
	}
	function createNewWorkspace() {
		openCreate();
	}

	function openEdit(workspace: WorkspaceInfo) {
		editingWorkspace = workspace;
		dialogueMode = 'edit';
		formName = editingWorkspace!.name;
		formColor = editingWorkspace!.color;
		dialogEl?.showModal();
	}

	function handleCreate() {
		let newWorkspace: WorkspaceInfo = {
			id: crypto.randomUUID().toString(),
			name: formName,
			color: formColor,
			owner: userStore.user!.full_name,
			role: 'owner'
		};
		workspaces.push(newWorkspace);
	}
	function handleEdit() {
		workspaces = workspaces.map((w) =>
			w.id === editingWorkspace?.id ? { ...w, name: formName, color: formColor } : w
		);
		editingWorkspace = null;
	}

	function handleSubmit(e: SubmitEvent) {
		console.log(formColor);
		e.stopPropagation();
		e.preventDefault();
		if (dialogueMode === 'create') {
			handleCreate();
		} else if (dialogueMode === 'edit') {
			handleEdit();
		}
		formName = '';
		formColor = '#4979E0';
		editingWorkspace = null;
		closeCreate();
	}
	function handleBackdrop(e: MouseEvent) {
		if (e.target === dialogEl) {
			closeCreate();
		}
	}

	function handleRemove(workspace: WorkspaceInfo) {
		workspaces = workspaces.filter((w) => w.id !== workspace.id);
	}
</script>

<h3>Workspaces</h3>
<span class="support-span">Manage Your Workspaces</span>
<div class="workspace-cards">
	{#each workspaces as workspace (workspace.id)}
		<WorkspaceCard {workspace} onDelete={handleRemove} onEdit={openEdit}></WorkspaceCard>
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
	<dialog class="new-workspace-form" bind:this={dialogEl} onclick={handleBackdrop}>
		<form onsubmit={handleSubmit}>
			<h1>{dialogueMode === 'create' ? 'Create New Workspace' : 'Edit Workspace'}</h1>
			<label class="name">
				<span>Name</span>
				<input
					class="inp"
					type="text"
					placeholder="Enter workspace name"
					required
					minlength="3"
					bind:value={formName}
				/>
			</label>
			<label class="color">
				<span>Color</span>
				<input class="color-inp" type="color" bind:value={formColor} />
			</label>
			<button class="submit" type="submit">
				{dialogueMode === 'create' ? 'Create New Workspace' : 'Confirm Edit'}
			</button>
			<button type="button" onclick={closeCreate}>Cancel</button>
		</form>
	</dialog>
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
		grid-auto-rows: 180px;
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
	.new-workspace-form * {
		box-sizing: border-box;
	}
	.new-workspace-form {
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
		padding: 2em;
		outline: none;
		border: 2px solid #d2d2d2;
		border-radius: 14px;
		align-items: center;
		background-color: white;
		> form {
			width: 100%;
		}
		> form > h1 {
			margin: 0;
			font-size: 18px;
			margin-bottom: 1em;
		}
		.name {
			display: flex;
			flex-direction: column;
			width: 100%;
			> span,
			> input {
				width: 100%;
			}
			.inp {
				border-radius: 8px;
				border: 1px solid #d1d1d1;
				padding: 4px 8px;
				height: 36px;
				margin-bottom: 8px;
			}
			> span {
				font-size: 14px;
				text-align: left;
				height: 18px;
				font-weight: 550;
				opacity: 70%;
			}
		}
		> form > button {
			border-radius: 8px;
			cursor: pointer;
			width: 100%;
			border: none;
			background-color: transparent;
		}
		> form > button:active {
			box-shadow: none;
		}
		> form > .submit {
			height: 40px;
			background-color: #005fb8;
			border: 1px solid #0051b8;
			color: white;
			box-shadow: 4px 4px 12px #aaaaaa;
		}
	}
	dialog:not([open]) {
		display: none;
	}
	dialog::backdrop {
		backdrop-filter: blur(2px);
	}

	.color {
		margin-bottom: 1em;
		width: 100%;
		> .color-inp {
			height: 28px;
			padding: 0;
			border: 1px solid #bdbdbd;
			border-radius: 8px;
			cursor: pointer;
			background: none;
			width: 100%;
			margin-bottom: 1em;
		}
		> span {
			font-size: 14px;
			text-align: left;
			height: 18px;
			font-weight: 550;
			opacity: 70%;
		}
	}
	input[type='color']::-webkit-color-swatch-wrapper {
		padding: 2px;
	}

	input[type='color']::-webkit-color-swatch {
		border: none;
		border-radius: 6px;
	}
</style>
