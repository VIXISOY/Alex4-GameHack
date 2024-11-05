import os
import signal
import ptrace.debugger

pid = int(input("Enter the PID of the process to trace: "))


debugger = ptrace.debugger.PtraceDebugger()

print("Attach the running process %s" % pid)

process = debugger.addProcess(pid, False)

def scan_memory_for_score(process, pid, score, previous_addresses=None):
    score_bytes = int(score).to_bytes(4, 'little')
    current_addresses = []

    with open(f"/proc/{pid}/maps", "r") as maps_file:
        for line in maps_file:
            if "rw" in line:  # Likely writable regions
                start_addr, end_addr = [int(x, 16) for x in line.split()[0].split('-')]

                with open(f"/proc/{pid}/mem", "rb") as mem_file:
                    mem_file.seek(start_addr)
                    region_data = mem_file.read(end_addr - start_addr)

                    # Search for all occurrences of score_bytes in the region
                    index = region_data.find(score_bytes)
                    while index != -1:
                        found_address = start_addr + index
                        current_addresses.append(found_address)
                        index = region_data.find(score_bytes, index + 1)

    # Compare current addresses with previous ones
    if previous_addresses is not None:
        stable_addresses = [addr for addr in current_addresses if addr in previous_addresses]
        print("Stable addresses from previous scan:")
        for address in stable_addresses:
            print(f"Address still containing score: {hex(address)}")
    else:
        stable_addresses = current_addresses  # For the first scan, all are "stable"

    # Print the current scan results
    print("Current scan results:")
    for address in current_addresses:
        print(f"Possible score address: {hex(address)}")

    return current_addresses, stable_addresses



def write_address(process, address, value, num_bytes=4):

    # Convert the integer value to bytes (little-endian format)
    value_bytes = value.to_bytes(num_bytes, 'little')
    # Write the bytes to the specified memory address
    process.writeBytes(address, value_bytes)
    print(f"Wrote value {value} to address {hex(address)}")


def read_address(process, address, num_bytes=4):
    
    # Read the specified number of bytes from the address
    data = process.readBytes(address, num_bytes)
    # Convert the bytes to an integer (assuming little-endian format)
    value = int.from_bytes(data, 'little')
    print(f"Value at address {hex(address)}: {value}")
    return value



def dump_stack_from_proc(pid):
    stack_info = ""
    with open(f"/proc/{pid}/maps", "r") as maps_file:
        for line in maps_file:
            if "stack" in line:
                stack_info = line.strip()
                break

    if stack_info:
        start_addr, end_addr = [int(x, 16) for x in stack_info.split()[0].split('-')]
        with open(f"/proc/{pid}/mem", "rb") as mem_file:
            mem_file.seek(start_addr)
            stack_data = mem_file.read(end_addr - start_addr)
            return stack_data
    return None

previous_addresses = None

while(True):
    
    command=input("Command (STOP/CONT/FIN/MAPS/STACK/SCAN/READ/WRITE)")
    if command=="STOP":
        os.kill(pid, signal.SIGSTOP)
    elif command=="CONT":
        os.kill(pid, signal.SIGCONT)
        process.detach()
    elif command=="MAPS":
        if process.is_attached==False:
            process = debugger.addProcess(pid, False)
        print(process.dumpMaps())
    elif command == "STACK":
        stack_dump = dump_stack_from_proc(pid)
        if stack_dump is not None:
            print("Stack Dump:")
            print(stack_dump)
        else:
            print("Could not find stack region.")
    elif command == "SCAN":
        current_addresses, stable_addresses = scan_memory_for_score(process,pid,input("Value:"), previous_addresses)
        previous_addresses = current_addresses
    elif command == "READ":
        if process.is_attached==False:
            process = debugger.addProcess(pid, False)
        score = read_address(process,int(input("Enter address to read (in hex, e.g. ): "), 16))
    elif command == "WRITE":
        if process.is_attached==False:
            process = debugger.addProcess(pid, False)
        print(process)
        score = write_address(process,int(input("Enter address to read (in hex, e.g.): "), 16),int(input("Enter Value:")))
    elif command=="FIN":
        break