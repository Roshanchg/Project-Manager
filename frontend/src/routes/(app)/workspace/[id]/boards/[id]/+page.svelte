<script lang="ts">
	import { page } from '$app/state';
	import { mockLists } from '$lib/api/lists';
	import { getBoardColor } from '$lib/boardColors';
	import ListColumn from '$lib/components/layout/ListColumn.svelte';
	import type { ListInfo } from '$lib/types';
	import { onMount } from 'svelte';

	const boardId = $derived(page.params.id);

	let listData = $state<ListInfo[]>(mockLists);

	$effect(() => {
		document.documentElement.style.setProperty('--colorFrom', getBoardColor(boardId!).from);
		document.documentElement.style.setProperty('--colorTo', getBoardColor(boardId!).to);
		return () => {
			document.documentElement.style.removeProperty('--colorFrom');
			document.documentElement.style.removeProperty('--colorFrom');
		};
	});

	let listDlg = $state<HTMLDialogElement | null>(null);
	let editingList = $state<ListInfo | null>(null);
	let formMode = $derived<'create' | 'edit'>(editingList === null ? 'create' : 'edit');
	let formListName = $state<string>('');

	function handleFormSubmit(e: SubmitEvent) {
		e.stopPropagation();
		e.preventDefault();
		switch (formMode) {
			case 'create':
				handleCreate();
				break;
			case 'edit':
				handleEdit();
				break;
		}
	}
	function openForm() {
		listDlg?.showModal();
	}
	function closeForm() {
		listDlg?.close();
		editingList = null;
		formListName = '';
	}
	function openEdit(list: ListInfo) {
		editingList = list;
		formListName = editingList.name;
		openForm();
	}
	function openCreate() {
		editingList = null;
		formListName = '';
		openForm();
	}
	function handleBackdrop(e: MouseEvent) {
		if (e.target === listDlg) {
			closeForm();
		}
	}
	function handleCreate() {
		let newList: ListInfo = {
			id: crypto.randomUUID(),
			name: formListName,
			position: listData.length,
			cards: []
		};
		listData.push(newList);
	}
	function handleEdit() {
		listData = listData.map((ld) =>
			ld.id === editingList?.id ? { ...ld, name: formListName } : ld
		);
	}
	function handleRemove(list: ListInfo) {
		listData = listData.filter((ld) => ld.id !== list?.id);
	}

	onMount(() => {});
</script>

<dialog class="new-list-dlg" bind:this={listDlg} onclick={handleBackdrop}>
	<form onsubmit={handleFormSubmit} class="list-form">
		<h1>{formMode === 'create' ? 'Insert New List' : 'Edit List'}</h1>
		<label class="name">
			<span>List Name</span>
			<input type="text" minlength="3" required bind:value={formListName} />
		</label>
		<button type="submit" class="submit-btn"
			>{formMode === 'create' ? 'Create New List' : 'Confirm Edit'}</button
		>
		<button type="reset" class="cancel-btn" onclick={closeForm}>Cancel</button>
	</form>
</dialog>

<h1
	style:--colorFrom={getBoardColor(boardId!).from}
	style:--colorTo={getBoardColor(boardId!).to}
	class="main-title"
>
	Board: {boardId}
</h1>
<div class="board-contents">
	{#each listData as list (list.id)}
		<ListColumn {list} onEdit={openEdit} onDelete={handleRemove} />
	{/each}
	<button class="new-list-btn" onclick={openCreate}>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			stroke-width="2"
			stroke="currentColor"
			class="size-6"
		>
			<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
		</svg>

		Add New List</button
	>
</div>

<style>
	.main-title {
		margin-top: 0;
	}
	:global(.right) {
		background: linear-gradient(
			135deg,
			color-mix(in srgb, var(--colorFrom) 50%, transparent) 0%,

			color-mix(in srgb, var(--colorTo) 50%, transparent) 60%
		);
	}

	.board-contents {
		display: flex;
		width: 100%;
		height: max-content;
		gap: 2em;
		align-items: flex-start;
		overflow-y: hidden;
		overflow-x: auto;
		padding-bottom: 1em;
	}
	.new-list-btn {
		display: flex;
		min-width: 16em;
		height: 8em;
		border-radius: 12px;
		border: 1px dashed gray;
		box-sizing: border-box;
		font-size: 1em;
		align-items: center;
		justify-content: center;
		color: #414141;
		font-weight: 550;
		cursor: pointer;
		background-color: #ffffff;
		> svg {
			height: 28px;
		}
	}

	.new-list-dlg {
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
		padding: 2em;
		outline: none;
		width: max-content;
		border: 2px solid #d2d2d2;
		border-radius: 14px;
		align-items: center;
		background-color: white;
	}
	.new-list-dlg:not([open]) {
		display: none;
	}
	.new-list-dlg::backdrop {
		backdrop-filter: blur(2px);
	}
	.list-form {
		display: flex;
		flex-direction: column;
		width: 100%;
		align-items: center;
		> h1 {
			margin: 0;
			margin-bottom: 1em;
			min-width: 16rem;
			text-align: center;
		}
		.name {
			margin-bottom: 1em;
			display: flex;
			flex-direction: column;
			width: 100%;
			> span {
				opacity: 70%;
				font-weight: 550;
				font-size: 14px;
			}
			> input {
				height: 30px;
			}
		}
		> button {
			width: 100%;
			height: 38px;
			border-radius: 8px;
			outline: none;
			cursor: pointer;
		}

		.submit-btn {
			background-color: #005fb8;
			border: 1px solid #0051b8;
			color: white;
			box-shadow: 4px 4px 12px #aaaaaa;
		}
		.cancel-btn {
			border: none;
			background-color: transparent;
		}
		.submit-btn:active {
			box-shadow: none;
		}
	}
</style>
