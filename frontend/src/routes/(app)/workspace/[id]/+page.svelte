<script lang="ts">
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import type{BoardInfo} from '$lib/types'
	import BoardCard from '$lib/components/layout/BoardCard.svelte';
	const  workspaceId=$derived(page.params.id)

	let boards=$state<BoardInfo[]>(
		[{
			id:"1",
			name:"Board 1",
			totalCards:10
		},
		{
			id:"2",
			name:"Board 2",
			totalCards:20

		},
		{
			id:"3",
			name:"Board 3",
			totalCards:30

		},
		{
			id:"4",
			name:"Board 4",
			totalCards:40

		},
		{
			id:"5",
			name:"Board 5",
			totalCards:50

		}
	]
	);

	
	let dialogEl=$state<HTMLDialogElement|null>(null);
	let editingBoard=$state<BoardInfo|null>(null);
	let dialogMode=$derived<"create"|"edit">((editingBoard===null) ? "create":"edit");
	let formBoardName=$state("");

	function openForm(){
		dialogEl?.showModal();
	}
	function closeForm(){
		editingBoard=null;
		formBoardName="";
		dialogEl?.close();
	}
	function handleBackdrop(e:MouseEvent){
		if (e.target===dialogEl){
			closeForm();
		}
	}
	function openCreate(){
		editingBoard=null;
		formBoardName="";
		openForm();
	}

	function handleCreate(){
		editingBoard=null;
		let newBoard:BoardInfo={
			id:crypto.randomUUID().toString(),
			name:formBoardName,
			totalCards:10,
		}
		boards.push(newBoard);
	}
	function openEdit(b:BoardInfo){
		editingBoard=b;
		formBoardName=editingBoard.name;
		openForm();
	}
	function handleEdit(){
		boards=boards.map((board)=>(board.id===editingBoard?.id) ? {...board,name:formBoardName}:board);
	}
	function handleRemove(b:BoardInfo){
		boards=boards.filter((board)=>b.id!==board.id);
	}
	function handleSubmit(e:SubmitEvent){
		e.stopPropagation();
		e.preventDefault();
		if (dialogMode==="create"){
			handleCreate();
		}
		else if(dialogMode==="edit"){
			handleEdit();
		}
		closeForm();
	}

    onMount(async ()=>{
    })
</script>

<h1>Workspace {workspaceId}</h1>
<dialog bind:this={dialogEl} onclick={handleBackdrop} class="form-dialog">
	<form onsubmit={handleSubmit} class="board-form" >
	<h1>{(dialogMode==="create" ? "Create New Board" : "Edit Board")}</h1>
	<label class="name">
		<span>Board name:</span>
		<input type="text" bind:value={formBoardName} minlength="3" placeholder="Board name here" required >
	</label>
		<button type="submit" class="submit-btn">{dialogMode==="create" ? "Create" : "Confirm Edit"}</button>
		<button type="reset" onclick={closeForm} class="cancel-btn">cancel</button>
	</form>

</dialog>
<div class="board-cards">
	{#each boards as board (board.id)}
		<BoardCard board={board} onEdit={openEdit}
		onDelete={handleRemove} 
		/>
	{/each}
	<button class="insert-card-btn" onclick={openCreate}>
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
		<span>Add New Board</span>
	</button>
</div>

<style>
	.board-cards{
		display: grid;
		grid-template-columns: repeat(auto-fill,minmax(300px,1fr));
		grid-auto-rows: 180px;
		gap: 1.4em;
	}
	.insert-card-btn {
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
	.insert-card-btn:hover {
		background-color: #f0f0f0;
	}
	.form-dialog{
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
	.form-dialog:not([open]){
		display: none;
	}
	.form-dialog::backdrop{
		backdrop-filter: blur(2px);
	}
	.board-form{
		display: flex;
		flex-direction: column;
		width: 100%;
		align-items: center;
		>h1{
			margin: 0;
			margin-bottom: 1em;
			min-width: 16rem;
			text-align: center;
		}
		.name{
			margin-bottom: 1em;
			display: flex;
			flex-direction: column;
			width: 100%;
			>span{
				opacity: 70%;
				font-weight: 550;
				font-size: 14px;
			}
			>input{
				height: 30px;
			}
		}	
		>button{
			width: 100%;
			height: 38px;
			border-radius: 8px;
			outline: none;
			cursor: pointer;
		}
		
		.submit-btn{
			background-color: #005fb8;
			border: 1px solid #0051b8;
			color: white;
			box-shadow: 4px 4px 12px #aaaaaa;
		}
		.cancel-btn{
			border: none; 
			background-color: transparent;
		}
		.submit-btn:active{
			box-shadow: none;
		}
	}
</style>
