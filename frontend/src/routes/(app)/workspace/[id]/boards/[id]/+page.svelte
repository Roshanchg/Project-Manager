<script lang="ts">
	import { page } from "$app/state";
	import { mockLists } from "$lib/api/lists";
	import { getBoardColor } from "$lib/boardColors";
	import ListColumn from "$lib/components/layout/ListColumn.svelte";
	import type { ListInfo } from "$lib/types";
	import { onMount } from "svelte";

    const boardId=$derived(page.params.id);

    let listData=$state<ListInfo[]>(mockLists);
    
    $effect(() => {
        document.documentElement.style.setProperty('--colorFrom', getBoardColor(boardId!).from);
        document.documentElement.style.setProperty('--colorTo', getBoardColor(boardId!).to);
        return () => {document.documentElement.style.removeProperty('--colorFrom');
        document.documentElement.style.removeProperty('--colorFrom');}
    });
    onMount(()=>{

    })
</script>
<h1 style:--colorFrom={getBoardColor(boardId!).from}
    style:--colorTo={getBoardColor(boardId!).to}
    class="main-title"
>Board: {boardId}</h1>
<div class="board-contents">
    {#each listData as list (list.id)}
        <ListColumn list={list} onEdit={(list:ListInfo)=>{console.log(list)}}
        onDelete={(list:ListInfo)=>{console.log(list)}} />
    {/each}
    
</div>

<style>
    .main-title{
        margin-top: 0;
    }
    :global(.right){
        background: linear-gradient(135deg, 
			color-mix(in srgb, var(--colorFrom) 50%, transparent) 0%,

		 	color-mix(in srgb, var(--colorTo) 50%, transparent) 60%);
    }
    
    .board-contents{
        display: flex;
        width: 100%;
        height:max-content;
        gap: 2em;
        align-items: flex-start;
        overflow-y: hidden;
        overflow-x:auto;
        padding-bottom: 1em;
    }
    
</style>