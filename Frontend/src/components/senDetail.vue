<template>
	<div :class="'bodyBox'">
		<el-collapse v-model="activeSentence" accordion :class="'collapseBox'" >
				<el-collapse-item v-for="(sen, index) in Sentences" 
				v-bind:name="sen.ID" :class="'sentenceBox'">
				<template #title v-if="activeSentence==sen.ID">
					<div :class="'titleBox'">
						<p>Sentence {{index+1}} Detail</p>
						<div>
						
								<div style="display: flex;">
									<el-tooltip effect="dark" content="Delete this sentence">
										<el-button type="info" :icon="Delete" 
										@click.stop="deleteSenClick"/>
									</el-tooltip>
									<el-tooltip effect="dark" content="Copy this sentence">
										<el-button type="info" :icon="CopyDocument" 
										@click.stop="clipSmallClick"/>
									</el-tooltip>
									<el-tooltip effect="dark" content="Generate this sentence">
										<el-button type="info" :icon="Refresh" 
										:loading="sen.senLoading" @click.stop="generateSenClick"/>
									</el-tooltip>
								</div>
						</div>
					</div>
					
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
							<el-skeleton :rows="0" v-if="sen.senLoading || sen.Text==''" animated ></el-skeleton>
							<p v-else>{{sen.Text}}</p>
						</div>
					</div>
					
				</template>
				<div :class="'SentenceBody'">
					<div :class="'relation'">
						<el-tag v-for="r in sen.Relation" 
						:class="'relationTag'" type="info" closable 
						:key="r" @close="closeTag(r)">
							{{r}}
						</el-tag>
						<el-button plain :icon="Plus" 
						:class="'relationTag'" @click="formVisible=true"></el-button>
					</div>
					<div :class="'SenText'">
						<el-skeleton :rows="2" v-if="sen.senLoading || sen.Text==''" animated ></el-skeleton>
						<el-input v-else v-model="sen.Text" 
						type="textarea" autosize></el-input>
					</div>
				</div>
				</el-collapse-item>
		</el-collapse>
		<div :class="'buttonSlip'">
			<el-button plain :icon="Plus" :class="'addButton'" 
			@click="addsenButtonClick">Add a sentence</el-button>
			<el-button plain :icon="CopyDocument" :class="'copyButton'" 
			@click="clipBigClick">Copy all sentences</el-button>
		</div>
	</div>
	
	<el-dialog v-model="formVisible" title="Add a Triple Set">
		<div :class="'inputBox'">
			<el-input v-model="tripleSet1" 
			placeholder="Word1" clearable :class="'input'"></el-input>
			<el-autocomplete v-model="tripleSet2"
			:fetch-suggestions="querySearch"
			clearable placeholder="Relation" :class="'input'"
			></el-autocomplete>
			<el-input v-model="tripleSet3"
			placeholder="Word2" clearable :class="'input'"></el-input>
		</div>

		<div :class="'formButton'">
			<el-button type="danger" round 
			@click="cancelButtonClick" :icon="Close">Cancel</el-button>
			<el-button type="success" round 
			@click="SaveButtonClick" :icon="Check">Confirm</el-button>
		</div>
	</el-dialog>
</template>

<script setup>
import useClipboard from "vue-clipboard3";
import {Delete, Plus, CopyDocument,Check,Close,Refresh} from '@element-plus/icons-vue'
import { ref,onMounted } from 'vue';
import {ElMessage } from 'element-plus' 
import axios from "axios";

const baseID = 1200

let activeSentence = ref(-1)

let tripleSet1 = ref('')
let tripleSet2 = ref('')
let tripleSet3 = ref('')
let count = 5

const recommends = ["main subject",'follow','have part', 'participant','location']
const recommendRelation = ref([])
let formVisible = ref(false)

const serverIP = "/api/hello"

let Sentences = ref([])

function constructRecom(){
	let ret = []
	for(var i=0;i<recommends.length;i++){
		ret.push({'value':recommends[i]})
	}
	return ret
}

function constructSenTest(){
	return [{
			ID:baseID+1,
			Relation: ["1 | 2 | 3", "4 | 5 | 6", "7 | 8 | 9", "10 | 11 | 12","13 | 14 | 15","16 | 17 | 18","19 | 20 | 21"],
			// Text: "This is the text data1"
			Text: '',
			senLoading:false
		},{
			ID:baseID+2,
			Relation: ["7 | 8 | 9","10 | 11 | 12"],
			Text: "This is the text data2",
			senLoading:false
		}]
}

onMounted(()=>{
	recommendRelation.value = constructRecom()
	Sentences.value = constructSenTest()
})

function findSen(idx){
	for (var i=0; i<Sentences.value.length; i++){
		if (Sentences.value[i].ID == idx){
			return i
		}
	}
	return -1
}

// 删除三元组Tag
function closeTag(tag){
	var curid = findSen(activeSentence.value)
	if (curid ==-1 ){
		return
	}
	Sentences.value[curid].Relation.splice(Sentences.value[curid].Relation.indexOf(tag),1)
}

// createFilter/querySearch 对el-autocomplete进行搜索
const createFilter = (queryString) => {
	return (words) =>{
		return (
			words.value.toLowerCase().indexOf(queryString.toLowerCase())===0
		)
	}
}

const querySearch = (queryString, cb) => {
	const results = queryString 
	? recommendRelation.value.filter(createFilter(queryString))
	:recommendRelation.value
	cb(results)
}

function SaveButtonClick(){
	if (tripleSet1.value=="" || tripleSet2.value == "" || tripleSet3.value == ""){
		cancelButtonClick()
		return
	}
	var tripleSet = tripleSet1.value+' | '+tripleSet2.value+' | '+tripleSet3.value
	var curid = findSen(activeSentence.value)
	
	Sentences.value[curid].Relation.push(tripleSet)
	tripleSet1.value = ""
	tripleSet2.value = ""
	tripleSet3.value = ""
	formVisible.value = false
}

function cancelButtonClick(){
	tripleSet1.value = ""
	tripleSet2.value = ""
	tripleSet3.value = ""
	formVisible.value = false
}

function addsenButtonClick(){
	count++
	var newid = baseID + count
	Sentences.value.push({
		ID: newid,
		Relation:[],
		Text:'',
		senLoading:false
	})
}

async function clipText(text){
	const { toClipboard } = useClipboard()
	try {
		await toClipboard(text)
		ElMessage("Copy to clipboard success, empty sentences is missed.")
	} catch(e){
		console.error(e)
	}
}

function clipBigClick(){
	var text = new String
	for (var i=0;i<Sentences.value.length;i++){
		text += Sentences.value[i].Text
	}
	clipText(text)
}

function clipSmallClick(){
	var curid = findSen(activeSentence.value)
	clipText(Sentences.value[curid].Text)
}

function deleteSenClick(){
	var curid = findSen(activeSentence.value)
	if (curid==-1){
		return
	}
	Sentences.value.splice(curid,1)
	activeSentence.value = -1
}

function generateSenClick(idx){
	// 1. get cur id
	var curid = findSen(activeSentence.value)
	
	// 2. generate post data
	const postData = {
		ID: Sentences.value[curid].ID,
		Relation: Sentences.value[curid].Relation
	}
	
	// 3. set loading state
	Sentences.value[curid].senLoading = true
	
	// 4. send request
	axios.post(serverIP,postData)
		 .then(function(response){
			 console.log(response.data)
			 // if success
			 console.log(response.data.Text)
			 let id = findSen(response.data.ID)
			 if (id == -1){
				 return
			 }
			 Sentences.value[id].Text = response.data.Text
			 Sentences.value[id].senLoading = false
			 
		 })
		 .catch(function(error){
			 console.error(error)
		 })
}



</script>

<style>
	
	.bodyBox{
		margin: auto;
		max-width: 80%;
		display: grid;
		gap: 8px;
	}
	
	.collapseBox{
		display: grid;
		gap: 8px;
	}
	
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
		/* height: 206px; */
		
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
		
/* 		border: 1px solid #525252;
		border-radius: 15px; */
		
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

	.inputBox{
		display: flex;
		gap: 15px;
		justify-content: center;
	}
	
	.input{
		width: auto;
	}

	.formButton{
		margin-top: 15px;
		text-align: right;
		padding-right: 6%;
	}

	.titleBox{
		display: flex;
	}
</style>