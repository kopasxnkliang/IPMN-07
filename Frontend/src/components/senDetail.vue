<template>
	<h1>{{Sentences}}</h1>
	<div >
		<el-collapse v-model="activeSentence" accordion @change="changeCollapse" >
				<el-collapse-item v-for="(sen, index) in Sentences" 
				
				v-bind:name="sen.ID" :class="'sentenceBox'">
				<template #title v-if="activeSentence==sen.ID">
					Sentence {{index+1}}
				</template>
				<template #title v-else >
					<div :class="'omittedBox'">
						<div :class="'omittedRelat'">
							<el-tag v-for="r in sen.Relation" 
							:class="'relationTag'" type="info" :key="r"> 
								{{r}} 
							</el-tag>
						</div>
						<div :class="'omittedText'">
							<el-skeleton :rows="0" v-if="sen.Text==''" animated ></el-skeleton>
							<p v-else>{{sen.Text}}</p>
						</div>
					</div>
					
				</template>
				<!-- {{sen}} -->
				<div :class="'SentenceBody'">
					<div :class="'relation'">
						<!-- <div v-for="r in sen.Relation" :class="'relationTag'">
							<p :class="'TripleSet'">{{r[0]}} | {{r[1]}} | {{r[2]}}</p>
							<el-button :icon="Delete" circle size="small" :class="'SetDeleteButton'"></el-button>
						</div> -->
						<el-tag v-for="r in ShowTag" 
						:class="'relationTag'" type="info" closable 
						:key="r" @close="closeTag(r)">
							{{r}}
						</el-tag>
						<el-button plain :icon="Plus" :class="'relationTag'"></el-button>
					</div>
					<div :class="'SenText'">
						<el-skeleton :rows="2" v-if="sen.Text==''" animated ></el-skeleton>
						<el-input v-else v-model="ShowText" 
						type="textarea" autosize></el-input>
					</div>
				</div>
				</el-collapse-item>
		</el-collapse>
		<div :class="'buttonSlip'">
			<el-button plain :icon="Plus" :class="'addButton'">Add a sentence</el-button>
			<el-button plain :icon="CopyDocument" :class="'copyButton'">Copy all sentences</el-button>
		</div>
	</div>
	
</template>

<script setup>
// import { defineComponent } from "vue";
import {Delete, Plus, CopyDocument} from '@element-plus/icons-vue'
import { ref } from 'vue';

const baseID = 1200

let activeSentence = ref(-1)
let lastSelectSen = -1
let ShowText = ref('')
let ShowTag = ref([])

let Sentences = [{
			ID:baseID+1,
			Relation: ["1 | 2 | 3", "4 | 5 | 6", "7 | 8 | 9", "10 | 11 | 12","13 | 14 | 15","16 | 17 | 18","19 | 20 | 21"],
			// Text: "This is the text data1"
			Text: ''
		},{
			ID:baseID+2,
			Relation: ["7 | 8 | 9","10 | 11 | 12"],
			Text: "This is the text data2"
		}]

// Sentences = [1,2,3]

function findSen(idx){
	for (var i=0; i<Sentences.length; i++){
		if (Sentences[i].ID == idx){
			return i
		}
	}
	return -1
}

// 在折叠面板中的输入框内修改, 切换后同步更新
function changeCollapse(){
	// window.console.error("inp",inp)
	// window.console.error("activeSentence",activeSentence)
	if (lastSelectSen==-1){
		let id = findSen(activeSentence.value)
		if (id==-1){
			return
		}
		// window.console.error(activeSentence.value,baseID,activeSentence.value - baseID)
		ShowText.value = Sentences[id].Text
		ShowTag.value = Sentences[id].Relation
		// window.console.error(ShowText.value)
		lastSelectSen = activeSentence.value
	} else{
		var lastSenid = findSen(lastSelectSen)
		var curid = findSen(activeSentence.value)
		if (lastSenid==-1 || curid==-1){
			return
		}
		Sentences[lastSenid].Text = ShowText.value
		Sentences[lastSenid].Relation = ShowTag.value
		ShowTag.value = Sentences[curid].Relation
		ShowText.value = Sentences[curid].Text
		lastSelectSen = activeSentence.value
	}
	// // alert(this)
	// window.console.error(this)
	
}

function closeTag(tag){
	window.console.error(tag, ShowTag.value.indexOf(tag))
	ShowTag.value.splice(ShowTag.value.indexOf(tag),1)
}
</script>

<style>
	.relationTag{
		display: flex;
		text-align: center;
		/* Set */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		padding: 6px 5px;
		gap: 5px;
		
		width: fit-content;
		height: 29px;
		
		border: 1px solid #000000;
		border-radius: 4px;
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 0;
		
	}
	
	.TripleSet{
		
		/* word1 | word2 | word3 */
		
		width: auto;
		height: 15px;
		
		font-family: 'Inter';
		font-style: normal;
		font-weight: 400;
		font-size: 12px;
		line-height: 15px;
		/* identical to box height */
		display: flex;
		align-items: center;
		
		color: #000000;
		
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 0;

	}
	
	.SetDeleteButton{
		/* image 2 */
		
		width: auto;
		height: auto;
				
		/* Inside auto layout */
		flex: none;
		order: 1;
		flex-grow: 0;

	}

	.relation{
		/* ↓ relation tripes [container] */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: flex-start;
		align-content: flex-start;
		padding: 4px;
		gap: 10px;
		
		width: 578.5px;
		height: 111px;
		
		border: 1px solid #D6D5D5;
		border-radius: 4px;
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 1;
	}

	.SentenceBody{
		/* sentence body */
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: flex-start;
		padding: 10px;
		gap: 10px;
		
		width: 1187px;
		height: 131px;
		
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		align-self: stretch;
		flex-grow: 0;
	}

	.SenText{
		/* sentence(loaded) */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: center;
		padding: 0px 4px;
		gap: 10px;
		
		width: 578.5px;
		height: 111px;
		
		border: 1px solid #D6D5C5;
		border-radius: 4px;
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		align-self: stretch;
		flex-grow: 1;

	}

	.sentenceBox{
		/* sentence 2(el-collapse) */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		padding: 10px 11px;
		
		width: 1209px;
		height: 206px;
		
		border: 1px solid #525252;
		border-radius: 15px;
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		flex-grow: 0;
		
	}

	.buttonSlip{
		/* Button slip */
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: center;
		padding: 0px;
		gap: 10px;
		
		width: 1209px;
		height: 65px;
		
		
		/* Inside auto layout */
		flex: none;
		order: 2;
		align-self: stretch;
		flex-grow: 0;
	}

	.addButton{
		/* Add button */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		padding: 3px 0px;
		
/* 		width: 1012px;
		height: 65px; */
		width: 80%;
		height: 100%;
		
		border: 1px solid #000000;
		border-radius: 10px;
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 1;		
		
			
		/* Add a sentence */
		
		font-family: 'Inter';
		font-style: normal;
		font-weight: 400;
		font-size: 15px;
		line-height: 18px;
		display: flex;
		align-items: center;
		text-align: center;
		
		color: #000000;

	}

	.copyButton{
		/* Copy button */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		padding: 3px 0px;
		
		width: 15%;
		height: 100%;
		
		border: 1px solid #000000;
		border-radius: 10px;
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		flex-grow: 0;
		
		/* Copy all sentences */
		
		font-family: 'Inter';
		font-style: normal;
		font-weight: 400;
		font-size: 15px;
		line-height: 18px;
		display: flex;
		align-items: center;
		text-align: center;
		
		color: #000000;

	}

	.omittedRelat{
		/* relation tripes */
		
		box-sizing: border-box;
		overflow: hidden;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: flex-start;
		padding: 21px 4px;
		gap: 10px;
		
		width: 45%;
		height: 70px;
		
		border: 1px solid #D6D5D5;
		border-radius: 4px;
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		align-self: stretch;
		flex-grow: 1;
	}

	.omittedBox{
		/* sentence 1 (el-collapse) */
		
		box-sizing: border-box;
		
		/* Auto layout */
		display: flex;
		flex-direction: row;
		align-items: center;
		padding: 10px 11px;
		gap: 10px;
		
		width: calc((100%)*2);
		height: 90px;
		
		border: 1px solid #525252;
		border-radius: 15px;
		
		/* Inside auto layout */
		flex: none;
		order: 0;
		flex-grow: 0;

	}

	.omittedText{
		/* sentence(loading) */
		
		width: 45%;
		height: 70px;
		
		
		/* Inside auto layout */
		flex: none;
		order: 1;
		flex-grow: 0;

	}
</style>