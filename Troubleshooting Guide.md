### Installing PyTorch

### Bugfixing

If you are using the GPU (which you probably should), add 
```
export CUDA_LAUNCH_BLOCKING=1
```
to the beginning of your script. This forces PyTorch to wait for CUDA operations to finish before continuing with Python code, allowing you to actually find out which line of your Code caused CUDA related issues.

Additionally, you can try running your code on the cpu `device="cpu"` to eliminate any issues with your CUDA setup as a potential source of errors.
0. Ask Google, StackOverflow or your preferred LLM
   - PyTorch is used by a lot of people, so you are probably not the only one with an issue.
   - Pasting the relevant part of an error message into a search engine is often enough to get helpful information.

1. Debug your Code!
   - You can use asserts, prints, etc for this.
   - A dedicated debugger tends to work best though.
   - Check if everything is as you expect it:
     - Sizes and dimensions of tensors (Also make sure the operations are done on the correct dimension)
     - Values within reasonable ranges (This can indicate numerical issues, problems with data, faulty operations in previous steps, ...)
     - Gradients that are missing or aren't deleted.
     - Hyperparameters creating weird or unexpected outcomes.
     - Tensor that should be a copy is actually a view (or vice versa)
     - ...
   - If you find something weird or unexpected, work backwards from there to find out what caused the issue.
     - Using a lot of asserts can work well here.
   - Ideally, you have now found the line(s) that cause the issue, if not...

2. Consult the [official documentation](https://docs.pytorch.org/docs/stable/index.html).
   - It's easy to make wrong assumptions about how certain functions operate and this is the best place to double check.
     - Common culprits are 
       - argument mix-ups
       - dimension issues (applying a function like mean() to a whole tensor instead of one dimension or vice versa)
       - issues with tensor dtypes
     
3. If that didn't solve the issue, [enabling debug mode](https://docs.pytorch.org/tutorials/recipes/debug_mode_tutorial.html) can be a next step.

4. Test if the issue is related to torch.compile by disabling it.
   - You can find information on troubleshooting issues with compile [here](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/compile/programming_model.observability.html).
   - As a last resort, simply disabling compile and accepting the performance loss is also a solution.

### Increasing Performance
_Check the performance guide for details on implementing these tweaks!_

##### General

- __Enable Tensor Cores__
  - This reduces memory usage and improves performance in almost all cases.
  - EXCEPTION: You really need the additional precision of 32bit float. In that case you probably know what you are doing anyway.
- __Use torch.compile__

##### Increasing GPU utilization
This is helpful if you notice that the GPU switches between loadspikes and idle phases (you can see this via nvtop).

- Only move things between CPU and GPU memory when necessary
- Use Multithreading to avoid Bottlenecks
- Use multiple workers in your Dataloader and pin the memory

##### Reducing Memory Load
This is helpful for avoiding those pesky ``CUDA Out of Memory`` exceptions.
- Adjust Hyperparameters (smaller Batches, smaller Models etc.)
- Use a Quantized version of your model if possible
- Finetune only part of your model if possible (LoRA for LLMs!)
- Remember to free up big tensors/models
- Avoid computing unnecessary gradients

If you are running into memory exceptions regardless, then there are two possible culprits:
- Your model is too big:
  - Use a bigger GPU
    - Talk to your Prof for access to NHR@FAU for some exclusive GPU access
  - Split the model onto multiple GPUs
    - If you are seriously considering this, check the documentation of your models library (i.e. transformers etc.)
    - Big models usually come with a multi GPU solution already implemented for you, you should use that
- Other people keep stealing your VRAM:
  - Run your code at less busy times (monday morning)
  - Talk to your Prof for access to NHR@FAU for some exclusive GPU access