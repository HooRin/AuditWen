import argparse
import json
import logging
import os
import tasks
import torch
from lm_eval import utils
import evaluator
from model_prompt import MODEL_PROMPT_MAP

logging.getLogger("openai").setLevel(logging.WARNING)
#auditmodel_4
#Qwen-7B-Chat
#chatglm3-6b
#gpt2
#auditmodel(3-30多卡7B)
#auditmodel(4-4多卡14B)
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--model_args", default="")
    parser.add_argument("--tasks", default=None, choices=utils.MultiChoice(tasks.ALL_TASKS))
    parser.add_argument("--model_prompt", default="no_prompt", choices=list(MODEL_PROMPT_MAP.keys()))
    parser.add_argument("--provide_description", action="store_true")
    parser.add_argument("--num_fewshot", type=int, default=5)
    parser.add_argument("--batch_size", type=str, default=128)
    parser.add_argument("--max_batch_size", type=int, default=None,
                        help="Maximal batch size to try with --batch_size auto")
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--output_path", default=None)
    parser.add_argument("--limit", type=float, default=None,
                        help="Limit the number of examples per task. "
                             "If <1, limit is a percentage of the total number of examples.")
    parser.add_argument("--data_sampling", type=float, default=None)
    parser.add_argument("--no_cache", action="store_true")
    parser.add_argument("--decontamination_ngrams_path", default=None)
    parser.add_argument("--description_dict_path", default=None)
    parser.add_argument("--check_integrity", action="store_true")
    parser.add_argument("--write_out", action="store_true", default=None)
    parser.add_argument("--output_base_path", type=str, default=None)
    parser.add_argument('--world_size', type=int, default=2)
    parser.add_argument('--trust_remote_code', default=True,action='store_true', help='Set to trust remote code')

    return parser.parse_args()


def main():
    args = parse_args()
    # 设置CUDA_VISIBLE_DEVICES
    os.environ["CUDA_VISIBLE_DEVICES"] = args.device if args.device else "0"  # 例如，如果 args.device 是 "0,1"

    assert not args.provide_description  # not implemented
    #torch.nn.DataParallel(args.model,device_ids=[0,1], output_device=None, dim=0)
    #if args.device:
    #    os.environ["CUDA_VISIBLE_DEVICES"] = args.device
    if args.limit:
        print(
            "WARNING: --limit SHOULD ONLY BE USED FOR TESTING. REAL METRICS SHOULD NOT BE COMPUTED USING LIMIT."
        )

    if args.tasks is None:
        task_names = tasks.ALL_TASKS
    else:
        task_names = utils.pattern_match(args.tasks.split(","), tasks.ALL_TASKS)

    print(f"Selected Tasks: {task_names}")

    description_dict = {}
    if args.description_dict_path:
        with open(args.description_dict_path, "r") as f:
            description_dict = json.load(f)

    results = evaluator.simple_evaluate(
        model=args.model,
        model_args=args.model_args,
        tasks=task_names,
        num_fewshot=args.num_fewshot,
        batch_size=args.batch_size,
        max_batch_size=args.max_batch_size,
        device=args.device,
        no_cache=args.no_cache,
        limit=args.limit,
        description_dict=description_dict,
        decontamination_ngrams_path=args.decontamination_ngrams_path,
        check_integrity=args.check_integrity,
        write_out=args.write_out,
        output_base_path=args.output_base_path,
        model_prompt=args.model_prompt,
        trust_remote_code=args.trust_remote_code
    )

    dumped = json.dumps(results, indent=2)
    print(dumped)

    if args.output_path:
        os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
        with open(args.output_path, "w") as f:
            f.write(dumped)

    batch_sizes = ",".join(map(str, results["config"]["batch_sizes"]))
    print(
        f"{args.model} ({args.model_args}), limit: {args.limit}, provide_description: {args.provide_description}, "
        f"num_fewshot: {args.num_fewshot}, batch_size: {args.batch_size}{f' ({batch_sizes})' if batch_sizes else ''}"
    )
    print(evaluator.make_table(results))


if __name__ == "__main__":
    main()
