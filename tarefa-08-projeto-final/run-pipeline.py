
from __future__ import annotations

import argparse

from collector import IPCollector, configure_logging, load_config
from processor import IPReportProcessor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Executa pipeline de IP enrichment.")
    parser.add_argument("--config", default="config.yaml")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    configure_logging(config.get("log_level", "INFO"), config.get("logs_dir", "./logs"))

    collector = IPCollector(
        ips=config["ips"],
        output_dir=config.get("output_dir", "./output"),
        max_retries=config.get("max_retries", 3),
        timeout=config.get("timeout", 10),
    )
    enriched_path = collector.run()

    processor = IPReportProcessor(
        input_path=enriched_path,
        output_path=f"{config.get('output_dir', './output')}/final_report.json",
    )
    final_path = processor.run()

    print(f"Pipeline concluído. Resultado final: {final_path}")


if __name__ == "__main__":
    main()
