# GPU 成本与容量决策

## 不只比较表面单价

同时估算全小时制、全包日和小时 pilot + 包日正式窗口。固定成本包括 API、持久存储与传输；GPU、API 和存储分别记账。

```text
hourly_expected = hourly_price × (pilot_hours + formal_hours)
                + fixed_costs
                + reacquire_probability × reacquire_impact

daily_expected  = daily_price × ceil((pilot_hours + formal_hours) / 24)
                + fixed_costs

hybrid_expected = hourly_price × pilot_hours
                + daily_price × ceil(formal_hours / 24)
                + fixed_costs
```

`reacquire_impact` 只填写有依据的重建、重复测试、延期或错过验收窗口损失；不确定时分别计算低、中、高情景，不制造伪精确数字。

## 推荐顺序

1. 本地 CPU/MPS 或便宜小 GPU 完成构建、接口、单步训练、保存/重载和恢复检查。
2. 目标 GPU 按小时完成一对真实端到端 Baseline/Reference pilot，记录训练、评分、重载和快照时间。
3. pilot 通过且协议冻结后，才购买正式连续窗口；若关机后容量不可保证，把容量保险计入决策。
4. 小 GPU 结果不用于替代目标 GPU 的性能、峰值显存或时间门。
5. 若没有下一项能减少硬阻塞的实验，达到止损线或恢复失败，暂停新消费。

运行 `python3 scripts/plan_capacity.py --help` 查看输入。工具只做透明算术比较；库存、退款、预约和报销资格仍需读取当前 provider 条款。
