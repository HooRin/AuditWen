from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

# Model names: "/model/AuditWen"
tokenizer = AutoTokenizer.from_pretrained( "/model/AuditWen", trust_remote_code=True)

# use auto mode, automatically select precision based on the device.
model = AutoModelForCausalLM.from_pretrained(
    " /model/AuditWen",
    device_map="auto",
    trust_remote_code=True
).eval()
#You can specify different generation length, top p and other related superparameters
model.generation_config = GenerationConfig.from_pretrained(" /model/AuditWen",, trust_remote_code=True, )  

# 1st dialogue turn
response, history = model.chat(tokenizer, "请问什么是审计范围?", history=None)
print(response)
#审计范围是指审计机构和审计人员在一定的审计目的和审计计划指导下，为完成审计任务所进行的审查所有事项。
#它包括审计对象、审计期间、以及对这些审计对象各个方面所进行的审查程度。

# 2nd dialogue turn
response, history = model.chat(tokenizer, "审计范围是指审计机构和审计人员在一定的审计目的和审计计划指导下，为完成审计任务所进行的审查所有事项。它包括审计对象、审计期间、以及对这些审计对象各个方面所进行的审查程度。", history=history)
print(response)
#微观经济政策是指中央银行为实现宏观经济目标而对企业、居民个人及各种金融性机构所制定并采取的各种政策。

