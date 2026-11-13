"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    relevant = [m['text'] for m in data['memories'] if m['owner'] == data['owner'] and m['tag'] == 'travel']
    def recall(arguments):
        if arguments['tag'] != 'travel':
            return {'facts': []}
        return {'facts': relevant}
    options = in_process_tool('recall', 'Retrieve this user\'s saved travel preferences.', {'tag': str}, recall) if agent.live else None
    answer = await agent.ask('travel', 'Use recall for relevant travel preferences; make no booking and do not infer availability.', {'request': data['request'], 'tag': 'travel'},
                             'Consider a train-based day trip with a quiet museum visit; verify schedules separately.', sdk=options)
    return {'retrieved_memory': relevant, 'answer': answer, 'owner': data['owner']}
