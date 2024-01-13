<script lang="ts">
    import '$lib/tailwind.css'
    import { browser } from '$app/environment';
    import { onMount, onDestroy } from 'svelte';

    enum Opcode {
        DESTROY,
        CREATE,
        SEND,
        NEW_RESPONSE,
        ADD_RESPONSE,
        FINISH_RESPONSE,
        TRANSLATE
    }
    
    let ws: WebSocket;
    let terms: [string, string][] = [];

    onMount(() => {
        if(!browser) return;
        ws = new WebSocket("ws://localhost:8765");

        ws.onopen = (e) => {
            console.log("Connected to server!");
            // Get a UUID for this client
            ws.send(JSON.stringify([Opcode.CREATE, ""]));
        }
        
        ws.onmessage = (e) => {
            console.log(e.data);
            let data = JSON.parse(e.data);
            switch (data[0]) {
                case Opcode.NEW_RESPONSE:
                    interviewerText = data[1];
                    break;
                case Opcode.ADD_RESPONSE:
                    interviewerText += data[1];
                    break;
                case Opcode.FINISH_RESPONSE:
                    let count = parseInt(data[1]);
                    if(count >= 5) {
                        onDone();
                    }
                    break;
                case Opcode.TRANSLATE:
                    for(let i = 0; i < data[1].length; i++) {
                        terms.push([data[1][i], Array.from(highlightedWords)[i]]);
                    }
                    terms = terms;
                    completeDialog.showModal();
                    break;
            }
        }
    })
    
    onDestroy(() => {
        if(!browser) return;
        ws.send(JSON.stringify([Opcode.DESTROY, ""]));
        ws.close();
    })

    let inputText: string;
    let customWord: string;
    let language: string;
    let langDialog: HTMLDialogElement;
    let completeDialog: HTMLDialogElement;

    function onKeyDown(e: KeyboardEvent) {
        if(e.key !== 'Enter') return;

        ws.send(JSON.stringify([Opcode.SEND, inputText]));
        inputText = "";
    }

    function customTextKey(e: KeyboardEvent) {
        if(e.key !== 'Enter') return;

        highlightedWords.add(customWord.replace(/[.,\/#!?$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase());
        customWord = "";
        highlightedWords = highlightedWords;
    }
    
    function langKeydown(e: KeyboardEvent) {
        if(e.key !== 'Enter') return;

        // create translator object taking nativeLanguage
        langDialog.close();
    }
    
    let interviewerText = "";
    $: words = interviewerText.split(" ").map(word => {
        return {
            word,
            highlighted: false
        }
    })

    let highlightedWords = new Set<string>();

    function toggleHighlight(word: string, highlighted: boolean) {
        let wordText = word.replace(/[.,\/#!?$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase();

        if(highlighted) highlightedWords.add(wordText);
        else highlightedWords.delete(wordText);
        highlightedWords = highlightedWords;
    }

    function onDone() {
        console.log("sending", Array.from(highlightedWords), "in", language)
        // translate the words
        ws.send(JSON.stringify([Opcode.TRANSLATE, { lang: language, words: Array.from(highlightedWords) }]));
    }

    onMount(() => {
        if(!browser) return;
        langDialog.showModal();
    })

    function goToMemoryCards() {
        let params = new URLSearchParams();
        params.set("terms", terms.map(term => term.join(",")).join(","));
        window.location.href = "/flashcards?" + params.toString();
    }
</script>

<style>
    .bg {
        background-color: rgb(31, 55, 135);
        background-image: url("/interviewer_smaller.png");
        background-repeat: no-repeat;
        background-position-x: center;
        background-position-y: bottom;
    }
</style>

<div class="w-screen h-screen bg">
    <div class="absolute top-0 left-0 m-8 rounded w-1/4 h-1/2 border-4 border-blue-300 p-3 bg-blue-100">
        <h2 class="w-full text-center text-xl p-0.5 font-bold text-black">
            Words to Learn List
            {#if highlightedWords.size > 0}
                ({highlightedWords.size})
            {/if}
        </h2>

        <input class="object-left-bottom focus:border-purple-300 border-4 border-blue-300 outline-none rounded p-2 m-2" type="text"
        on:keydown={customTextKey} bind:value={customWord}
        placeholder="Enter a custom word..." />
        
        {#each highlightedWords as word}
            <div>{word}</div>
        {/each}
        
    </div>
    <div class="absolute top-0 right-0 m-8 rounded w-1/3 h-1/2 border-4 border-blue-300 p-3 overflow-y-auto bg-blue-100">
        <h2 class="w-full text-center text-xl p-2 font-bold text-black">
            Interviewer
        </h2>
        {#each words as word}
            <span>
                <button class="hover:text-red-400 cursor-pointer inline-block"
                class:text-red-700={word.highlighted} class:font-bold={word.highlighted}
                on:click={() => {
                    word.highlighted = !word.highlighted
                    toggleHighlight(word.word, word.highlighted)
                }}>
                    {@html word.word.replace('\n', '<br />')}
                </button>
            </span>
        {/each}
    </div>
    <div class="w-full absolute bottom-0 flex flex-col items-center">
        <input class="focus:border-purple-300 outline-none rounded p-2 m-2 w-1/2 bg-blue-100 border-4 border-blue-300" type="text"
        on:keydown={onKeyDown} bind:value={inputText}
        placeholder="Type your answer here..." />
    </div>
</div>

<dialog class="p-5"
on:close|preventDefault bind:this={langDialog}>
    <input class="object-left-bottom focus:border-purple-300 outline-none rounded p-2 m-2 bg-blue-100 border-4 border-blue-300"
    type="text"
    on:keydown={langKeydown} bind:value={language}
    placeholder="Enter native language"/>
</dialog> 

<dialog class="rounded p-5 flex flex-row border-4 border-blue-300" bind:this={completeDialog} on:close|preventDefault>
    <table>
        <tr>
            <th>Word</th>
            <th>Translation</th>
        </tr>
        {#each terms as term}
            <tr>
                <td>{term[1]}</td>
                <td>{term[0]}</td>
            </tr>
        {/each}
    </table>
    <button on:click={goToMemoryCards}
    class="hover:border-purple-300 p-4 rounded bg-blue-100 border-blue-300">
        Memory Cards Review
    </button>
</dialog>