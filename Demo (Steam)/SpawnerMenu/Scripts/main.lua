local scriptsDir = [[D:\SteamLibrary\steamapps\common\Militsioner Demo\TallProject\Binaries\Win64\ue4ss\Mods\SpawnerMenu\Scripts]]
local commandFile = scriptsDir .. [[\cmd.txt]]
local guiScript = scriptsDir .. [[\GUI.exe]]

-- Unreal Engine Spawner Script with Python GUI Bridge
local function ResolveClass(path, name)
    local cls = nil
    
    -- 1. Try to find it if it's already loaded in memory
    if path and path ~= "" then 
        cls = StaticFindObject(path) 
    end
    
    -- 2. If not in memory, FORCE LOAD it from the pak files
    if not cls or not cls:IsValid() then
        if path and path ~= "" then
            print("Class not in memory, attempting to force load from disk: " .. path)
            -- Remove the _C temporarily to load the raw package if needed
            local packagePath = string.gsub(path, "%.[^%.]+_C$", "")
            
            -- Attempt to load the raw asset package into memory
            local loadedAsset = LoadAsset(packagePath)
            if loadedAsset and loadedAsset:IsValid() then
                print("Asset loaded into memory successfully.")
            end
            
            -- Now search for the actual Class object again
            cls = StaticFindObject(path)
        end
    end
    
    -- 3. Fallback to just the name if the path was completely wrong
    if not cls or not cls:IsValid() then
        local searchName = name
        if string.sub(searchName, -2) ~= "_C" then searchName = searchName .. "_C" end
        cls = StaticFindObject(searchName)
    end
    
    return cls
end

local function TrySpawn(path, itemName)
    -- MUST BE WRAPPED IN GAME THREAD TO SPAWN ACTORS
    ExecuteInGameThread(function()
        local player = FindFirstOf("PlayerController")
        if not player or not player:IsValid() then 
            print("Error: Player not found")
            return 
        end
        
        local world = player:GetWorld()
        if not world or not world:IsValid() then 
            print("Error: World not found")
            return 
        end
        
        local classObj = ResolveClass(path, itemName)
        if not classObj or not classObj:IsValid() then 
            print("Error: Failed to load class " .. tostring(itemName))
            return 
        end

        local cameraManager = player.PlayerCameraManager
        if cameraManager and cameraManager:IsValid() then
            local loc = cameraManager:GetCameraLocation()
            local rot = cameraManager:GetCameraRotation()
            local pitch = math.rad(rot.Pitch)
            local yaw = math.rad(rot.Yaw)
            
            -- Push item 300 units forward in front of the camera
            loc.X = loc.X + (math.cos(pitch) * math.cos(yaw) * 300)
            loc.Y = loc.Y + (math.cos(pitch) * math.sin(yaw) * 300)
            loc.Z = loc.Z + (math.sin(pitch) * 300)

            local spawned = world:SpawnActor(classObj, loc, rot)
            if spawned and spawned:IsValid() then
                print("Successfully Spawned: " .. tostring(itemName))
            else
                print("Error: Unreal Engine refused to spawn the object (may be abstract or restricted).")
            end
        end
    end)
end

-- Listener Loop to read commands from the Python GUI
LoopAsync(500, function()
    local cmdPath = commandFile
    
    local file = io.open(cmdPath, "r")
    if file then
        local content = file:read("*all")
        file:close()
        
        -- Strip any hidden newline characters the python script might add
        content = content:gsub("\r", ""):gsub("\n", "")
        
        if content and content ~= "" then
            local name, path = content:match("([^|]+)|([^|]+)")
            if name and path then
                print("Python requested spawn: " .. name)
                TrySpawn(path, name)
            end
            
            -- Clear file immediately after reading
            local clearFile = io.open(cmdPath, "w")
            if clearFile then clearFile:write("") clearFile:close() end
        end
    end
    return false
end)

-- Hotkey to open Python window
RegisterKeyBind(Key.F4, function()
    print("[SpawnerMenu] F4 received")

    local file = io.open(guiScript, "r")
    if not file then
        print("[SpawnerMenu] GUI.py not found: " .. guiScript)
        return
    end
    file:close()

    print("[SpawnerMenu] Launching: " .. guiScript)

    local command = 'start "" "' .. guiScript .. '"'
    local result, reason, code = os.execute(command)

    print("[SpawnerMenu] Launcher result: "
        .. tostring(result) .. ", "
        .. tostring(reason) .. ", "
        .. tostring(code))
end)

print("Python Spawner Bridge Loaded. Press F4 to open.")
