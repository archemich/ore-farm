<script lang="ts">
    import { Terminal } from '@xterm/xterm';
    
    const terminal = new Terminal();
    let prompt = '';
     
    function openTerminal(node: Element){
        terminal.open(node);
    }

    function writeTerminal(e: Event) {
        terminal.write(prompt);
        prompt="";
    }
    
</script>

<div class="termianl">
    <form on:submit|preventDefault={writeTerminal}>
        <input bind:value={prompt} type="text" name="prompt"/>
    </form>
    <div use:openTerminal></div>

</div>
