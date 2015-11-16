#! /usr/bin/python

import sys, os
import collections
import argparse
from itertools import takewhile

# An unscheduled task
unsched_task_t = collections.namedtuple('unsched_task_t', 'name priority')
# A scheduled task
sched_task_t = collections.namedtuple('sched_task_t', 'cmd auto_mask cores props')
# Process properties
proc_props_t = collections.namedtuple('proc_props_t', 'energy phase l1misses l2misses sharing')

#-----------------------------------------------------
# Task ID to command mapping code
g_task_db = ({
    'blackscholes-sm':'$PARSEC_APPS_PATH/blackscholes/inst/amd64-linux.gcc/bin/blackscholes 4 $PARSEC_APPS_PATH/blackscholes/inputs/in_4K.txt /tmp/blackscholes-sm.out',
    'blackscholes-md':'$PARSEC_APPS_PATH/blackscholes/inst/amd64-linux.gcc/bin/blackscholes 4 $PARSEC_APPS_PATH/blackscholes/inputs/in_16K.txt /tmp/blackscholes-md.out',
    'blackscholes-lg':'$PARSEC_APPS_PATH/blackscholes/inst/amd64-linux.gcc/bin/blackscholes 4 $PARSEC_APPS_PATH/blackscholes/inputs/in_64K.txt /tmp/blackscholes-lg.out',
    'fluidanimate-sm':'$PARSEC_APPS_PATH/fluidanimate/inst/amd64-linux.gcc/bin/fluidanimate 4 4 $PARSEC_APPS_PATH/fluidanimate/inputs/in_35K.fluid /tmp/fluidanimate-sm.out',
    'fluidanimate-md':'$PARSEC_APPS_PATH/fluidanimate/inst/amd64-linux.gcc/bin/fluidanimate 4 4 $PARSEC_APPS_PATH/fluidanimate/inputs/in_100K.fluid /tmp/fluidanimate-md.out',
    'fluidanimate-lg':'$PARSEC_APPS_PATH/fluidanimate/inst/amd64-linux.gcc/bin/fluidanimate 4 4 $PARSEC_APPS_PATH/fluidanimate/inputs/in_300K.fluid /tmp/fluidanimate-lg.out',
    'facesim-sm':'sh $PARSEC_APPS_PATH/facesim/inst/amd64-linux.gcc/bin-sm/run_facesim.sh',
    'facesim-md':'sh $PARSEC_APPS_PATH/facesim/inst/amd64-linux.gcc/bin-md/run_facesim.sh',
    'facesim-lg':'sh $PARSEC_APPS_PATH/facesim/inst/amd64-linux.gcc/bin-lg/run_facesim.sh',
    'swaptions-sm':'$PARSEC_APPS_PATH/swaptions/inst/amd64-linux.gcc/bin/swaptions -nt 4 -sm 1024 -ns 4',
    'swaptions-md':'$PARSEC_APPS_PATH/swaptions/inst/amd64-linux.gcc/bin/swaptions -nt 4 -sm 5120 -ns 16',
    'swaptions-lg':'$PARSEC_APPS_PATH/swaptions/inst/amd64-linux.gcc/bin/swaptions -nt 4 -sm 10240 -ns 64',
    'x264-sm':'$PARSEC_APPS_PATH/x264/inst/amd64-linux.gcc/bin/x264 --threads 4 --bitrate 2048 -o /tmp/x264-sm.out $PARSEC_APPS_PATH/x264/inputs/eledream_640x360_8.y4m',
    'x264-md':'$PARSEC_APPS_PATH/x264/inst/amd64-linux.gcc/bin/x264 --threads 4 --bitrate 2048 -o /tmp/x264-md.out $PARSEC_APPS_PATH/x264/inputs/eledream_640x360_32.y4m',
    'x264-lg':'$PARSEC_APPS_PATH/x264/inst/amd64-linux.gcc/bin/x264 --threads 4 --bitrate 2048 -o /tmp/x264-lg.out $PARSEC_APPS_PATH/x264/inputs/eledream_640x360_128.y4m',
    'raytrace':'$PARSEC_APPS_PATH/raytrace/inst/amd64-linux.gcc/bin/rtview $PARSEC_APPS_PATH/raytrace/inputs/happy_buddha.obj',
	'vips-sm':'$PARSEC_APPS_PATH/vips/inst/amd64-linux.gcc/bin/vips --vips-concurrency=4 im_benchmark $PARSEC_APPS_PATH/vips/inputs/pomegranate_1600x1200.v output.v',
    'vips-md':'$PARSEC_APPS_PATH/vips/inst/amd64-linux.gcc/bin/vips --vips-concurrency=4 im_benchmark $PARSEC_APPS_PATH/vips/inputs/vulture_2336x2336.v output.v',
    'vips-lg':'$PARSEC_APPS_PATH/vips/inst/amd64-linux.gcc/bin/vips --vips-concurrency=4 im_benchmark $PARSEC_APPS_PATH/vips/inputs/bigben_2662x5500.v output.v',
    'bodytrack-sm':'$PARSEC_APPS_PATH/bodytrack/inst/amd64-linux.gcc/bin/bodytrack $PARSEC_APPS_PATH/bodytrack/inputs/sequenceB_1 1 1 1 1 0 4 1',
	'bodytrack-md':'$PARSEC_APPS_PATH/bodytrack/inst/amd64-linux.gcc/bin/bodytrack $PARSEC_APPS_PATH/bodytrack/inputs/sequenceB_2 1 1 1 1 0 4 1',  
	'bodytrack-lg':'$PARSEC_APPS_PATH/bodytrack/inst/amd64-linux.gcc/bin/bodytrack $PARSEC_APPS_PATH/bodytrack/inputs/sequenceB_4 1 1 1 1 0 4 1',
	'freqmine-sm':'$PARSEC_APPS_PATH/freqmine/inst/amd64-linux.gcc/bin/freqmine /home/student/parsec-3.0/pkgs/apps/freqmine/inputs/kosarak_250k.dat 220',
	'freqmine-md':'$PARSEC_APPS_PATH/freqmine/inst/amd64-linux.gcc/bin/freqmine /home/student/parsec-3.0/pkgs/apps/freqmine/inputs/kosarak_500k.dat 220',
	'freqmine-lg':'$PARSEC_APPS_PATH/freqmine/inst/amd64-linux.gcc/bin/freqmine /home/student/parsec-3.0/pkgs/apps/freqmine/inputs/kosarak_990k.dat 220',
});

#-----------------------------------------------------
# Task ID to command mapping code
g_props_db = ({
    'blackscholes-sm':  proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'blackscholes-md':  proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'blackscholes-lg':  proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'fluidanimate-sm':  proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'fluidanimate-md':  proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'fluidanimate-lg':  proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'facesim-sm':       proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'facesim-md':       proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'facesim-lg':       proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'swaptions-sm':     proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'swaptions-md':     proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'swaptions-lg':     proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'x264-sm':          proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'x264-md':          proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'x264-lg':          proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'raytrace':         proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'vips-sm':          proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'vips-md':          proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'vips-lg':          proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'bodytrack-sm':     proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'bodytrack-md':     proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'bodytrack-lg':     proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'freqmine-sm':      proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'freqmine-md':      proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
    'freqmine-lg':      proc_props_t(energy=0,phase=0,l1misses=0,l2misses=0,sharing=0),
});

#-----------------------------------------------------
# Properties to log
#
# Two formats supported:
# 1) string: Will lookup the string value as a path in out db
# 2) tuple of (name, filter_function, list): Will lookup the items for
#    the values in list and apply an accumulator function to them.
#    Example: ('sum_abc', lambda acc,x:acc+x, ['a', 'b', 'c'] will log:
#             db['a']+db['b']+db['c']

accumulate = lambda acc,x:acc+x
g_props_to_log = ([
    'phase',
    ('time', accumulate, ['time/init','time/bound','time/weave']),
    'beefy/beefy-0/cycles',
    'beefy/beefy-0/cCycles',
    'beefy/beefy-0/instrs',
    'beefy/beefy-1/cycles',
    'beefy/beefy-1/cCycles',
    'beefy/beefy-1/instrs',
    'wimpy/wimpy-0/cycles',
    'wimpy/wimpy-0/cCycles',
    'wimpy/wimpy-0/instrs',
    'wimpy/wimpy-1/cycles',
    'wimpy/wimpy-1/cCycles',
    'wimpy/wimpy-1/instrs',
    ('l1_beefy-0/hits', accumulate, [x+'_beefy/'+x+'_beefy-0/'+y for x in ['l1i','l1d'] for y in ['hGETS','hGETX','fhGETS','fhGETX']]),
    ('l1_beefy-1/hits', accumulate, [x+'_beefy/'+x+'_beefy-1/'+y for x in ['l1i','l1d'] for y in ['hGETS','hGETX','fhGETS','fhGETX']]),
    ('l1_wimpy-0/hits', accumulate, [x+'_wimpy/'+x+'_wimpy-0/'+y for x in ['l1i','l1d'] for y in ['hGETS','hGETX','fhGETS','fhGETX']]),
    ('l1_wimpy-1/hits', accumulate, [x+'_wimpy/'+x+'_wimpy-1/'+y for x in ['l1i','l1d'] for y in ['hGETS','hGETX','fhGETS','fhGETX']]),
    ('l1_beefy-0/misses', accumulate, [x+'_beefy/'+x+'_beefy-0/'+y for x in ['l1i','l1d'] for y in ['mGETS','mGETXIM','mGETXSM']]),
    ('l1_beefy-1/misses', accumulate, [x+'_beefy/'+x+'_beefy-1/'+y for x in ['l1i','l1d'] for y in ['mGETS','mGETXIM','mGETXSM']]),
    ('l1_wimpy-0/misses', accumulate, [x+'_wimpy/'+x+'_wimpy-0/'+y for x in ['l1i','l1d'] for y in ['mGETS','mGETXIM','mGETXSM']]),
    ('l1_wimpy-1/misses', accumulate, [x+'_wimpy/'+x+'_wimpy-1/'+y for x in ['l1i','l1d'] for y in ['mGETS','mGETXIM','mGETXSM']]),
    ('l2_beefy-0/hits', accumulate, ['l2_beefy/l2_beefy-0/'+x for x in ['hGETS','hGETX']]),
    ('l2_beefy-1/hits', accumulate, ['l2_beefy/l2_beefy-1/'+x for x in ['hGETS','hGETX']]),
    ('l2_wimpy-0/hits', accumulate, ['l2_wimpy/l2_wimpy-0/'+x for x in ['hGETS','hGETX']]),
    ('l2_wimpy-1/hits', accumulate, ['l2_wimpy/l2_wimpy-1/'+x for x in ['hGETS','hGETX']]),
    ('l2_beefy-0/misses', accumulate, ['l2_beefy/l2_beefy-0/'+x for x in ['mGETS','mGETXIM','mGETXSM']]),
    ('l2_beefy-1/misses', accumulate, ['l2_beefy/l2_beefy-1/'+x for x in ['mGETS','mGETXIM','mGETXSM']]),
    ('l2_wimpy-0/misses', accumulate, ['l2_wimpy/l2_wimpy-0/'+x for x in ['mGETS','mGETXIM','mGETXSM']]),
    ('l2_wimpy-1/misses', accumulate, ['l2_wimpy/l2_wimpy-1/'+x for x in ['mGETS','mGETXIM','mGETXSM']]),
]);

#-----------------------------------------------------
# Command line option parser
g_schedulers = ['auto','1b','1s','bb','ss','bs','bss','bbs','fair'];

#-----------------------------------------------------
# Core mapping
g_core_map = ({
	'beefy-0':'0', 'beefy-1':'1', 'wimpy-0':'2', 'wimpy-1':'3',
});

def get_options():
    parser = argparse.ArgumentParser(description='Simulate QuickIA in ZSim')
    parser.add_argument('command', type=str, nargs=1, choices=['generate', 'run', 'help'], help='What should the script do?')
    parser.add_argument('--hp_tasks', type=str, default=None, help='High priority tasks to run.')
    parser.add_argument('--lp_tasks', type=str, default=None, help='Ligh priority tasks to run.')
    parser.add_argument('--scheduler', type=str, default='fair', choices=g_schedulers, help='Scheduling algorithm')
    parser.add_argument('--template', type=str, default='quickia.cfg.tmpl', help='zsim config template')
    parser.add_argument('--out_cfg', type=str, default='quickia.cfg', help='Output zsim config file')
    parser.add_argument('--log', type=str, default=None, help='Output log file')
    return parser.parse_args()

def print_usage_help():
    print 'TODO'

#-----------------------------------------------------
# Generate a zsim configuration file
# tmpl_path: Path to a zsim cfg file template (cfg file without process info)
# cfg_path: Path to output cfg file
# tasks: List of sched_task_t. Contains commands and core affinities 

def generate_zsim_cfg(tmpl_path, cfg_path, tasks):
    cfg_file = open(cfg_path, 'w')
    cfg_file.write(open(tmpl_path, 'r').read());
    taskid = 0
    for task in tasks:
        task_name = 'process' + str(taskid)
        if task.auto_mask == 1:
            task_entry = (task_name + ' = {\n' +
                          '    command = "' + task.cmd + '";\n' +
                          '    mask = "' + ' '.join(g_core_map[c] for c in task.cores) + '";\n' +
                          '};\n')
        else:
            task_entry = (task_name + ' = {\n' +
                          '    command = "' + task.cmd + '";\n' +
                          '    energy = ' + str(task.props.energy) + ';\n' +
                          '    phase = ' + str(task.props.phase) + ';\n' +
                          '    l1misses = ' + str(task.props.l1misses) + ';\n' +
                          '    l2misses = ' + str(task.props.l2misses) + ';\n' +
                          '    sharing = ' + str(task.props.sharing) + ';\n' +
                          '};\n')
        cfg_file.write(task_entry)
        taskid = taskid + 1
    cfg_file.close()

#-----------------------------------------------------
# Generate a task to core mapping based on given schedule
# Not for the "auto" scheduler

def gen_manual_task_to_core_schedule(unsched_tasks, scheduler):
    hp_core_db = ({
        '1b'   : ['beefy-0'],
        '1s'   : ['wimpy-0'],
        'bb'   : ['beefy-0','beefy-1'],
        'ss'   : ['wimpy-0','wimpy-1'],
        'bs'   : ['beefy-0','wimpy-0'],
        'bbs'  : ['beefy-0','beefy-1','wimpy-0'],
        'bss'  : ['beefy-0','wimpy-0','wimpy-1'],
        'fair' : ['beefy-0','beefy-1','wimpy-0','wimpy-1']
    });
    lp_core_db = ({
        '1b'   : ['wimpy-0'],
        '1s'   : ['beefy-0'],
        'bb'   : ['wimpy-0','wimpy-1'],
        'ss'   : ['beefy-0','beefy-1'],
        'bs'   : ['beefy-1','wimpy-1'],
        'bbs'  : ['wimpy-1'],
        'bss'  : ['beefy-1'],
        'fair' : ['beefy-0','beefy-1','wimpy-0','wimpy-1']
    });

    sched_tasks = []    
    for task in unsched_tasks:
        if task.name not in g_task_db:
            print 'ERROR: Could not find a command for task ' + task.name + '. Supported tasks:'
            print '\n'.join(sorted(g_task_db.keys()))
            sys.exit(1)
        if (task.priority == 'hp'):
            cores=hp_core_db[scheduler]
        else:
            cores=lp_core_db[scheduler]
        sched_tasks.append(sched_task_t(cmd=g_task_db[task.name], auto_mask=1, cores=cores, props=''))
    return sched_tasks

#-----------------------------------------------------
# Generate a parameters for zsim to compute core affinities
# Only for the "auto" scheduler

def gen_auto_task_to_core_schedule(unsched_tasks):
    sched_tasks = []    
    for task in unsched_tasks:
        if task.name not in g_task_db:
            print 'ERROR: Could not find a command for task ' + task.name + '. Supported tasks:'
            print '\n'.join(sorted(g_task_db.keys()))
            sys.exit(1)
        sched_tasks.append(sched_task_t(cmd=g_task_db[task.name], auto_mask=0, cores=[0], props=g_props_db[task.name]))
    return sched_tasks

#-----------------------------------------------------
# Parse zsim.out file

is_tab = ' '.__eq__
def parse_zsim_out(zout_path):
    lines = iter(open(zout_path, 'r').readlines())
    zout_dict = dict()
    stack = []
    for line in lines:
        line = line.partition('#')[0].rstrip()
        path = line.partition(':')[0].rstrip()
        val = line.partition(':')[2].lstrip()
        indent = len(list(takewhile(is_tab, path)))
        stack[indent:] = [path.lstrip()]
        if (stack[0] == 'root' and val != ''):
            zout_dict['/'.join(stack[1:])] = int(val)
    return zout_dict

#-----------------------------------------------------
# Write CSV log file

def write_log(log_path, scheduler, hp_tasks, lp_tasks):
    header = (['scheduler','hp_tasks','lp_tasks'] +
              map(lambda x:x[0] if isinstance(x,tuple) else x, g_props_to_log))
    zout_db = parse_zsim_out('zsim.out')
    log_hdl = None
    if os.path.isfile(log_path):
        log_hdl = open(log_path, 'a')
    else:
        log_hdl = open(log_path, 'w')
        log_hdl.write(','.join(header) + '\n')
    logline = scheduler
    logline += ',' + (hp_tasks if hp_tasks is not None else '<None>')
    logline += ',' + (lp_tasks if lp_tasks is not None else '<None>')
    for prop in g_props_to_log:
        if isinstance(prop, tuple):
            value = reduce(prop[1], map(lambda x:zout_db[x], prop[2]))
        else:
            value = zout_db[prop]
        logline += ',' + str(value)
    log_hdl.write(logline + '\n')
    log_hdl.close()

#-----------------------------------------------------
# Main

def main():
    # Parse args
    args = get_options();
    cmd = args.command[0];

    if (cmd == 'help'):
        print_usage_help();
        sys.exit(0)

    # Gather a list of tasks to run
    unsched_tasks = []
    if args.hp_tasks is not None:
        for task in args.hp_tasks.split(','):
            unsched_tasks.append(unsched_task_t(name=task, priority='hp'))
    if args.lp_tasks is not None:
        for task in args.lp_tasks.split(','):
            unsched_tasks.append(unsched_task_t(name=task, priority='lp'))
    if (not unsched_tasks):
        print 'ERROR: No tasks to simulate. Specify the hp_tasks or lp_tasks option.'
        sys.exit()

    if not os.environ.get('PARSEC_APPS_PATH'):
        print 'ERROR: env variable PARSEC_APPS_PATH not defined. Please define it to point to the parsec pkgs/apps dir.'
        sys.exit(1)

    # Generate a task-to-core mapping
    if args.scheduler == 'auto':
        sched_tasks = gen_auto_task_to_core_schedule(unsched_tasks)
    else:
        sched_tasks = gen_manual_task_to_core_schedule(unsched_tasks, args.scheduler)

    # Generate zsim cfg file
    if (cmd in ['generate', 'run']):
        generate_zsim_cfg(args.template, args.out_cfg, sched_tasks)

    if (cmd in ['run']):
        # Run ZSim
        os.system('../build/opt/zsim ' + args.out_cfg)
        # Parse zsim output file
        if (args.log is not None):
            write_log(args.log, args.scheduler, args.hp_tasks, args.lp_tasks)


if __name__ == '__main__':
    main()
