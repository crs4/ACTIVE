# Copyright (c) 2015, CRS4 S.R.L.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its 
# contributors may be used to endorse or promote products derived 
# from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
# THE POSSIBILITY OF SUCH DAMAGE.
# reference to the main celery instance

from __future__ import absolute_import
from job_processor.celery import app


"""
This module is used to define a generic evaluator function for sequential skeletons.
This function is a Celery task that will be instantiated and executed remotely 
in some cluster node.
Actually distributed evaluation is available only for sequential skeletons.
"""

# wrapper function necessary to execute tasks through celery
@app.task
def eval_distributed(skeleton, values):
	"""
	@param skeleton: Sequential skeleton contining the function to compute in a distributed way with provided arguments.
	@type skeleton: Seq
	@param values: Input data for the computation.
	@type values: List of objects
	@return: The result of Seq skeleton evaluation.
	@rtype: Object
	"""
	return skeleton.execute(values)
