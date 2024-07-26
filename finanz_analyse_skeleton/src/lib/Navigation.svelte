<script lang="ts" context="module">
	import { writable, type Writable } from 'svelte/store';

	export type SubPage = {
		href: string;
		name: string;
	};

	export let sub_pages: Writable<SubPage[]> = writable([]);
</script>

<nav class="list-nav">
	<ul>
		{#each $sub_pages as sub_page}
			<li><a href={sub_page.href}>{sub_page.name}</a></li>
		{/each}
	</ul>
</nav>
