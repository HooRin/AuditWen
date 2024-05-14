import json
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

def dump_json(dataset, name):
    f = open(name + '.json', "w", encoding="utf-8")
    json.dump(dataset, f, ensure_ascii=False)
    f.close()

def loadData(json_file_path):
    json_answer = []
    t = 0
    # 使用 with 语句打开文件，确保文件关闭
    with open(json_file_path, 'r', encoding='utf-8') as file:
        # 使用 json.load() 方法加载 JSON 数据
        data = json.load(file)

    tokenizer = AutoTokenizer.from_pretrained("",trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("",device_map="auto", trust_remote_code=True).eval()
    model.generation_config = GenerationConfig.from_pretrained("", trust_remote_code=True, )  # 可指定不同的生成长度、top_p等相关超参

    for i in data:
        response, history = model.chat(tokenizer, i['query'], history=None)
        #print(response)
        data_test = {
            "question": i["query"],
            "answer": i['answer'],
            "prediction": response,
        }
        json_answer.append(data_test)
        
    # 创建一个DataFrame对象
    df = pd.DataFrame(json_answer)
    df.to_excel("",index=False)
    dump_json(json_answer,"")

if __name__ == '__main__':

    filename1 = ""
    selected_sentences = loadData(filename1)









